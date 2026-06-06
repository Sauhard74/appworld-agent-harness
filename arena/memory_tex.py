"""Tex-backed memory store.

Tex is used ONLY as the semantic retriever over instructions. The verbatim
code BODIES are kept locally so that the Tex and local backends return
identical Demo bodies for the same retrieved task_ids -- isolating retrieval
quality for a fair A/B comparison.
"""
import re

from arena.memory import Demo, MemoryStore

# Marker we embed in stored turn text so the task_id survives Tex's wrapper
# (e.g. "[Date: ...] [user] [[task_id]] <instruction>") and can be parsed back.
_MARKER_RE = re.compile(r"\[\[(?P<tid>[^\]]+)\]\]")

# Fixed ISO timestamp -- Tex ordering is by semantic score, not time.
_TS = "2026-01-01T00:00:00Z"


def _build_client():
    from tex import Tex
    from arena import config
    return Tex(
        api_key=config.TEX_API_KEY,
        base_url=config.TEX_BASE_URL,
        org_id=config.TEX_ORG_ID,
        user_id=config.TEX_USER_ID,
    )


class TexMemoryStore(MemoryStore):
    def __init__(self, client=None, session_id=None):
        self._client = client
        self._session_id = session_id
        self._by_key: dict[str, Demo] = {}

    @property
    def client(self):
        if self._client is None:
            self._client = _build_client()
        return self._client

    @property
    def session_id(self):
        if self._session_id is None:
            from arena import config
            self._session_id = config.TEX_SESSION_ID
        return self._session_id

    @staticmethod
    def _turn_text(demo: Demo):
        return f"[[{demo.task_id}]] {demo.instruction}"

    def add(self, demo: Demo):
        self._by_key[demo.task_id] = demo
        self.client.conversations.remember(
            session_id=self.session_id,
            turns=[{"role": "user", "text": self._turn_text(demo), "timestamp": _TS}],
        )

    def add_many(self, demos):
        demos = list(demos)
        if not demos:
            return
        turns = []
        for demo in demos:
            self._by_key[demo.task_id] = demo
            turns.append({"role": "user", "text": self._turn_text(demo), "timestamp": _TS})
        self.client.conversations.remember(session_id=self.session_id, turns=turns)

    def recall(self, instruction, k, exclude_task_id=None):
        r = self.client.recall(q=instruction, session_id=self.session_id)
        out = []
        seen = set()
        for turn in getattr(getattr(r, "hits", None), "turns", []) or []:
            text = getattr(turn, "text", None)
            if not text:
                continue
            m = _MARKER_RE.search(text)
            if not m:
                continue
            tid = m.group("tid")
            if tid == exclude_task_id or tid in seen:
                continue
            demo = self._by_key.get(tid)
            if demo is None:
                continue
            seen.add(tid)
            out.append(demo)
            if len(out) >= k:
                break
        return out
