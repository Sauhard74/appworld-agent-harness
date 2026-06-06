import json

from arena.memory import Demo
from arena.memory_hydra import HydraMemoryStore


class _Chunk:
    """Mimics hydra_db V2Chunk: carries metadata + chunk_content + relevancy_score."""

    def __init__(self, task_id, instruction, relevancy_score, with_metadata=True):
        self.relevancy_score = relevancy_score
        self.chunk_content = f"[[{task_id}]] {instruction}"
        self.metadata = {"task_id": task_id} if with_metadata else None


class _Data:
    def __init__(self, chunks):
        self.chunks = chunks


class _QueryResponse:
    def __init__(self, chunks):
        self.success = True
        self.data = _Data(chunks)


class _Context:
    def __init__(self, fake):
        self._fake = fake

    def ingest(self, tenant_id=None, type=None, memories=None):
        self._fake.ingests.append(
            {"tenant_id": tenant_id, "type": type, "memories": json.loads(memories)}
        )


class FakeHydra:
    """Fake HydraDB client. context.ingest() records; query() returns preset chunks."""

    def __init__(self, query_chunks):
        self.ingests = []
        self.context = _Context(self)
        self._query_chunks = query_chunks
        self.query_calls = []

    def query(self, tenant_id=None, query=None, type=None, mode=None, max_results=None):
        self.query_calls.append(
            {"tenant_id": tenant_id, "query": query, "type": type,
             "mode": mode, "max_results": max_results}
        )
        return _QueryResponse(self._query_chunks)


def test_recall_returns_bodies_in_score_order():
    chunks = [
        _Chunk("t2", "play edm songs", 1.9),
        _Chunk("t1", "buy apples", 1.1),
    ]
    store = HydraMemoryStore(client=FakeHydra(chunks), tenant_id="t")
    store.add(Demo("t1", "buy apples", "bodyA"))
    store.add(Demo("t2", "play edm songs", "bodyB"))

    out = store.recall("electronic dance music", k=5)
    assert [d.task_id for d in out] == ["t2", "t1"]
    assert [d.body for d in out] == ["bodyB", "bodyA"]


def test_recall_honors_exclude_task_id():
    chunks = [
        _Chunk("t2", "play edm songs", 1.9),
        _Chunk("t1", "buy apples", 1.1),
    ]
    store = HydraMemoryStore(client=FakeHydra(chunks), tenant_id="t")
    store.add_many([Demo("t1", "buy apples", "bodyA"), Demo("t2", "play edm songs", "bodyB")])

    out = store.recall("anything", k=5, exclude_task_id="t2")
    assert [d.task_id for d in out] == ["t1"]


def test_recall_k_caps_results():
    chunks = [
        _Chunk("t3", "c", 1.9),
        _Chunk("t2", "b", 1.8),
        _Chunk("t1", "a", 1.7),
    ]
    store = HydraMemoryStore(client=FakeHydra(chunks), tenant_id="t")
    store.add_many([Demo("t1", "a", "A"), Demo("t2", "b", "B"), Demo("t3", "c", "C")])

    out = store.recall("anything", k=2)
    assert len(out) == 2
    assert [d.task_id for d in out] == ["t3", "t2"]


def test_recall_skips_unmatched_or_unparseable_chunks():
    chunks = [
        _Chunk("ghost", "not stored", 1.9),                 # parses but no stored demo
        _Chunk("t1", "buy apples", 1.1),
    ]
    store = HydraMemoryStore(client=FakeHydra(chunks), tenant_id="t")
    store.add(Demo("t1", "buy apples", "bodyA"))

    out = store.recall("anything", k=5)
    assert [d.task_id for d in out] == ["t1"]


def test_recall_recovers_task_id_from_marker_when_metadata_missing():
    # No metadata -> task_id recovered from the [[task_id]] marker in chunk_content.
    chunks = [_Chunk("t1", "buy apples", 1.1, with_metadata=False)]
    store = HydraMemoryStore(client=FakeHydra(chunks), tenant_id="t")
    store.add(Demo("t1", "buy apples", "bodyA"))

    out = store.recall("anything", k=5)
    assert [d.task_id for d in out] == ["t1"]
    assert [d.body for d in out] == ["bodyA"]


def test_add_many_one_ingest_call_per_demo():
    # Mirror Tex: each demo ingested in its own call (one memory item each).
    fake = FakeHydra([])
    store = HydraMemoryStore(client=fake, tenant_id="t")
    store.add_many([Demo("t1", "a", "A"), Demo("t2", "b", "B")])
    assert len(fake.ingests) == 2
    assert all(len(call["memories"]) == 1 for call in fake.ingests)
    # both task_id markers present (order nondeterministic -- calls run concurrently)
    texts = "".join(call["memories"][0]["text"] for call in fake.ingests)
    assert "[[t1]]" in texts and "[[t2]]" in texts
    # infer disabled for raw semantic storage
    assert all(call["memories"][0]["infer"] is False for call in fake.ingests)
