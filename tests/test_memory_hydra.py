"""Tests for HydraMemoryStore (raw-httpx backend). No network: we stub the
two REST primitives (_ingest, _query) and exercise the pure mapping logic."""
from arena.memory import Demo
from arena.memory_hydra import HydraMemoryStore


def _store():
    return HydraMemoryStore(api_key="k", base_url="http://x", tenant_id="t")


def _chunk(task_id=None, content="", score=0.0):
    meta = {"task_id": task_id} if task_id is not None else {}
    return {"metadata": meta, "chunk_content": content, "relevancy_score": score}


def test_recall_returns_bodies_in_query_order():
    s = _store()
    s._by_key = {"t1": Demo("t1", "buy apples", "BODY_A"),
                 "t2": Demo("t2", "play edm", "BODY_B")}
    s._query = lambda instruction, k: [_chunk("t2", score=0.9), _chunk("t1", score=0.4)]
    out = s.recall("music", k=2)
    assert [d.task_id for d in out] == ["t2", "t1"]
    assert [d.body for d in out] == ["BODY_B", "BODY_A"]


def test_recall_excludes_task_id():
    s = _store()
    s._by_key = {"t1": Demo("t1", "a", "A"), "t2": Demo("t2", "b", "B")}
    s._query = lambda instruction, k: [_chunk("t1"), _chunk("t2")]
    out = s.recall("q", k=5, exclude_task_id="t1")
    assert [d.task_id for d in out] == ["t2"]


def test_recall_caps_at_k():
    s = _store()
    s._by_key = {f"t{i}": Demo(f"t{i}", "x", f"B{i}") for i in range(5)}
    s._query = lambda instruction, k: [_chunk(f"t{i}") for i in range(5)]
    assert len(s.recall("q", k=3)) == 3


def test_recall_task_id_from_marker_fallback():
    # metadata missing -> recover task_id from the [[task_id]] marker in content
    s = _store()
    s._by_key = {"t9": Demo("t9", "inst", "BODY9")}
    s._query = lambda instruction, k: [_chunk(None, content="[Date: x] [[t9]] inst")]
    out = s.recall("q", k=1)
    assert out and out[0].task_id == "t9"


def test_recall_skips_unmatched_chunks():
    s = _store()
    s._by_key = {"t1": Demo("t1", "a", "A")}
    s._query = lambda instruction, k: [_chunk("ghost"), _chunk("t1")]
    out = s.recall("q", k=5)
    assert [d.task_id for d in out] == ["t1"]


def test_add_many_one_ingest_per_demo_concurrent(monkeypatch):
    s = _store()
    calls = []
    monkeypatch.setattr(s, "_ingest", lambda demo: calls.append(demo.task_id))
    monkeypatch.setattr(s, "ensure_tenant", lambda *a, **k: True)
    monkeypatch.setattr(s, "_wait_until_indexed", lambda *a, **k: True)
    s.add_many([Demo("t1", "a", "A"), Demo("t2", "b", "B"), Demo("t3", "c", "C")])
    assert sorted(calls) == ["t1", "t2", "t3"]
    assert set(s._by_key) == {"t1", "t2", "t3"}
