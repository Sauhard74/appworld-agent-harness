from arena.memory import Demo
from arena.memory_tex import TexMemoryStore


class _Turn:
    def __init__(self, score, text):
        self.score = score
        self.text = text


class _Hits:
    def __init__(self, turns):
        self.turns = turns


class _RecallResult:
    def __init__(self, turns, confidence=1.0):
        self.hits = _Hits(turns)
        self.confidence = confidence


class _Conversations:
    def __init__(self, fake):
        self._fake = fake

    def remember(self, session_id=None, turns=None):
        self._fake.remembered.append({"session_id": session_id, "turns": turns})


class FakeTex:
    """Fake Tex client. remember() records; recall() returns preset turns.

    The recalled turns mimic Tex wrapping stored text:
      "[Date: ...] [user] [[task_id]] <instruction>"
    in a chosen (score) order.
    """

    def __init__(self, recall_turns):
        self.remembered = []
        self.conversations = _Conversations(self)
        self._recall_turns = recall_turns
        self.recall_calls = []

    def recall(self, q=None, session_id=None):
        self.recall_calls.append({"q": q, "session_id": session_id})
        return _RecallResult(self._recall_turns)


def _wrap(task_id, instruction, ts="2026-01-01T00:01:00Z"):
    return f"[Date: {ts}] [user] [[{task_id}]] {instruction}"


def test_recall_returns_bodies_in_score_order():
    # Tex returns t2 ahead of t1 by score.
    turns = [
        _Turn(0.9, _wrap("t2", "play edm songs")),
        _Turn(0.5, _wrap("t1", "buy apples")),
    ]
    store = TexMemoryStore(client=FakeTex(turns), session_id="s")
    store.add(Demo("t1", "buy apples", "bodyA"))
    store.add(Demo("t2", "play edm songs", "bodyB"))

    out = store.recall("electronic dance music", k=5)
    assert [d.task_id for d in out] == ["t2", "t1"]
    assert [d.body for d in out] == ["bodyB", "bodyA"]


def test_recall_honors_exclude_task_id():
    turns = [
        _Turn(0.9, _wrap("t2", "play edm songs")),
        _Turn(0.5, _wrap("t1", "buy apples")),
    ]
    store = TexMemoryStore(client=FakeTex(turns), session_id="s")
    store.add_many([Demo("t1", "buy apples", "bodyA"), Demo("t2", "play edm songs", "bodyB")])

    out = store.recall("anything", k=5, exclude_task_id="t2")
    assert [d.task_id for d in out] == ["t1"]


def test_recall_k_caps_results():
    turns = [
        _Turn(0.9, _wrap("t3", "c")),
        _Turn(0.8, _wrap("t2", "b")),
        _Turn(0.7, _wrap("t1", "a")),
    ]
    store = TexMemoryStore(client=FakeTex(turns), session_id="s")
    store.add_many([Demo("t1", "a", "A"), Demo("t2", "b", "B"), Demo("t3", "c", "C")])

    out = store.recall("anything", k=2)
    assert len(out) == 2
    assert [d.task_id for d in out] == ["t3", "t2"]


def test_recall_skips_unmatched_or_unparseable_turns():
    turns = [
        _Turn(0.9, _wrap("ghost", "not stored")),   # parses but no stored demo
        _Turn(0.8, "[Date: x] [user] no marker here"),  # unparseable
        _Turn(0.7, _wrap("t1", "buy apples")),
    ]
    store = TexMemoryStore(client=FakeTex(turns), session_id="s")
    store.add(Demo("t1", "buy apples", "bodyA"))

    out = store.recall("anything", k=5)
    assert [d.task_id for d in out] == ["t1"]


def test_add_many_one_remember_call_per_demo():
    # A single giant batch hangs the live Tex API, so add_many ingests each demo
    # in its own remember() call (one turn each).
    fake = FakeTex([])
    store = TexMemoryStore(client=fake, session_id="s")
    store.add_many([Demo("t1", "a", "A"), Demo("t2", "b", "B")])
    assert len(fake.remembered) == 2
    assert all(len(call["turns"]) == 1 for call in fake.remembered)
    # both task_id markers present (order is nondeterministic — calls run concurrently)
    texts = "".join(call["turns"][0]["text"] for call in fake.remembered)
    assert "[[t1]]" in texts and "[[t2]]" in texts
