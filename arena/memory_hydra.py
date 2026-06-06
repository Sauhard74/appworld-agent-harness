"""HydraDB-backed memory store.

HydraDB is used ONLY as the semantic retriever over instructions. The verbatim
code BODIES are kept locally so that the Hydra, Tex, and local backends return
identical Demo bodies for the same retrieved task_ids -- isolating retrieval
quality for a fair A/B comparison.

Real API discovered live (hydra_db SDK / api.hydradb.com, api_version=2):
  - ingest:  client.context.ingest(tenant_id=..., type="memory",
               memories=json.dumps([{"text":..., "infer": False,
                                      "metadata": {"task_id": ...}}]))
             Ingestion is async (queued); chunks become queryable shortly after.
  - query:   client.query(tenant_id=..., query=..., type="memory",
                           mode="fast", max_results=k)
             -> resp.data.chunks : list[V2Chunk] ranked by relevancy_score desc.
             Each chunk has .metadata ({"task_id": ...}), .chunk_content, .relevancy_score.

We carry task_id in chunk metadata (primary) AND embed a [[task_id]] marker in
the stored text (fallback) -- mirroring the Tex backend -- so recovery is robust.
"""
import json
import re

from arena.memory import Demo, MemoryStore

# Marker embedded in stored text so task_id survives even if metadata is absent.
_MARKER_RE = re.compile(r"\[\[(?P<tid>[^\]]+)\]\]")


def _build_client():
    from hydra_db import HydraDB
    from arena import config
    return HydraDB(token=config.HYDRADB_API_KEY)


class HydraMemoryStore(MemoryStore):
    def __init__(self, client=None, tenant_id=None):
        self._client = client
        self._tenant_id = tenant_id
        self._by_key: dict[str, Demo] = {}

    @property
    def client(self):
        if self._client is None:
            self._client = _build_client()
        return self._client

    @property
    def tenant_id(self):
        if self._tenant_id is None:
            from arena import config
            self._tenant_id = config.HYDRADB_TENANT_ID
        return self._tenant_id

    @staticmethod
    def _memory_text(demo: Demo):
        return f"[[{demo.task_id}]] {demo.instruction}"

    def add(self, demo: Demo):
        self._by_key[demo.task_id] = demo
        memories = [{
            "text": self._memory_text(demo),
            "infer": False,
            "metadata": {"task_id": demo.task_id},
        }]
        self.client.context.ingest(
            tenant_id=self.tenant_id,
            type="memory",
            memories=json.dumps(memories),
        )

    def add_many(self, demos, max_workers=16):
        # One ingest() call per demo (mirrors Tex: a single giant batch can hang
        # the live API). Fire concurrently -- calls are independent.
        from concurrent.futures import ThreadPoolExecutor
        demos = list(demos)
        if not demos:
            return
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            list(ex.map(self.add, demos))

    @staticmethod
    def _chunk_task_id(chunk):
        # Prefer metadata; fall back to the [[task_id]] marker in the text.
        meta = getattr(chunk, "metadata", None) or {}
        tid = meta.get("task_id") if isinstance(meta, dict) else None
        if tid:
            return tid
        text = getattr(chunk, "chunk_content", None) or ""
        m = _MARKER_RE.search(text)
        return m.group("tid") if m else None

    def recall(self, instruction, k, exclude_task_id=None):
        resp = self.client.query(
            tenant_id=self.tenant_id,
            query=instruction,
            type="memory",
            mode="fast",
            max_results=max(k, 1),
        )
        data = getattr(resp, "data", None)
        chunks = getattr(data, "chunks", None) or []
        out = []
        seen = set()
        for chunk in chunks:
            tid = self._chunk_task_id(chunk)
            if not tid or tid == exclude_task_id or tid in seen:
                continue
            demo = self._by_key.get(tid)
            if demo is None:
                continue
            seen.add(tid)
            out.append(demo)
            if len(out) >= k:
                break
        return out
