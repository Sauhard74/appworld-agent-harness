"""HydraDB-backed memory store (bonus backend).

Implemented with raw httpx, NOT the hydradb-sdk: the SDK pins pydantic v2, which
conflicts with AppWorld's pydantic v1. We call the documented REST API directly
(base https://api.hydradb.com, auth header x-api-key, api_version 2).

Like the Tex backend, HydraDB is used ONLY as a semantic retriever over
instructions; verbatim code BODIES are kept locally in self._by_key so every
backend returns identical Demo bodies (fair A/B). task_id round-trips via the
chunk's metadata, with a [[task_id]] text marker as a fallback.

REST shape (verified against the SDK source + live):
  - POST /tenants            json {"tenant_id"}                      (create)
  - GET  /tenants/status     params {"tenant_id"} -> data.infra.ready_for_ingestion
  - POST /context/ingest     multipart form: type=memory, tenant_id, upsert,
                             memories=json([{text, infer, metadata}])  (async)
  - POST /query              json {tenant_id, query, type, mode, max_results}
                             -> data.chunks[] : {chunk_content, relevancy_score, metadata}
"""
import json
import re
from concurrent.futures import ThreadPoolExecutor

from arena.memory import Demo, MemoryStore

_MARKER_RE = re.compile(r"\[\[(?P<tid>[^\]]+)\]\]")


class HydraMemoryStore(MemoryStore):
    def __init__(self, api_key=None, base_url=None, tenant_id=None, timeout=30.0):
        from arena import config
        self.api_key = api_key or config.HYDRADB_API_KEY
        self.base_url = (base_url or config.HYDRADB_BASE_URL).rstrip("/")
        self.tenant_id = tenant_id or config.HYDRADB_TENANT_ID
        self.timeout = timeout
        self._by_key: dict[str, Demo] = {}
        self._http = None

    @property
    def http(self):
        if self._http is None:
            import httpx
            self._http = httpx.Client(
                base_url=self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=self.timeout,
            )
        return self._http

    # ---- REST primitives -------------------------------------------------
    def ensure_tenant(self, wait_s=120):
        """Create the tenant if missing and block until ready for ingestion."""
        import time
        try:
            self.http.post("/tenants", json={"tenant_id": self.tenant_id})
        except Exception:
            pass  # already exists / conflict is fine
        for _ in range(max(1, int(wait_s / 3))):
            try:
                r = self.http.get("/tenants/status", params={"tenant_id": self.tenant_id})
                infra = (r.json().get("data", {}) or {}).get("infra", {}) or {}
                if infra.get("ready_for_ingestion"):
                    return True
            except Exception:
                pass
            time.sleep(3)
        return False

    def _ingest(self, demo: Demo):
        # multipart/form-data: each field sent as a (None, value) form part.
        memories = json.dumps([{
            "text": f"[[{demo.task_id}]] {demo.instruction}",
            "infer": False,
            "metadata": {"task_id": demo.task_id},
        }])
        files = {
            "type": (None, "memory"),
            "tenant_id": (None, self.tenant_id),
            "upsert": (None, "true"),
            "memories": (None, memories),
        }
        self.http.post("/context/ingest", files=files)

    def _query(self, instruction, k):
        """Return the raw list of chunk dicts ranked by relevancy."""
        r = self.http.post("/query", json={
            "tenant_id": self.tenant_id,
            "query": instruction,
            "type": "memory",
            "mode": "fast",
            "max_results": max(k * 3, k),  # over-fetch; dedupe/exclude below
        })
        return (r.json().get("data", {}) or {}).get("chunks", []) or []

    # ---- MemoryStore interface ------------------------------------------
    def add(self, demo: Demo):
        self._by_key[demo.task_id] = demo
        self._ingest(demo)

    def add_many(self, demos, max_workers=16):
        demos = list(demos)
        if not demos:
            return
        self.ensure_tenant()
        for d in demos:               # register bodies locally first (free)
            self._by_key[d.task_id] = d
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            list(ex.map(self._ingest, demos))
        self._wait_until_indexed(demos)

    def _wait_until_indexed(self, demos, wait_s=120):
        """Ingestion is async; block until a sentinel demo is queryable."""
        import time
        sentinel = demos[0]
        for _ in range(max(1, int(wait_s / 3))):
            try:
                for ch in self._query(sentinel.instruction, k=5):
                    if self._chunk_task_id(ch) in self._by_key:
                        return True
            except Exception:
                pass
            time.sleep(3)
        return False

    @staticmethod
    def _chunk_task_id(chunk):
        meta = chunk.get("metadata") or {}
        tid = meta.get("task_id") if isinstance(meta, dict) else None
        if tid:
            return tid
        m = _MARKER_RE.search(chunk.get("chunk_content", "") or "")
        return m.group("tid") if m else None

    def recall(self, instruction, k, exclude_task_id=None):
        out, seen = [], set()
        for ch in self._query(instruction, k):
            tid = self._chunk_task_id(ch)
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
