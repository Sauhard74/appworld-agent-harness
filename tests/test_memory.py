import numpy as np
from arena.memory import LocalTrajectoryStore, Demo

def _fake_embed(texts):
    # deterministic 2-d embedding: count of 'a' and 'b'
    return [np.array([t.lower().count("a"), t.lower().count("b")], float) for t in texts]

def test_recall_returns_most_similar():
    store = LocalTrajectoryStore(embed_fn=_fake_embed)
    store.add(Demo("t1", "aaa apples", "codeA"))
    store.add(Demo("t2", "bbb bananas", "codeB"))
    out = store.recall("aaaa", k=1)
    assert len(out) == 1 and out[0].task_id == "t1"

def test_recall_excludes_self_by_task_id():
    store = LocalTrajectoryStore(embed_fn=_fake_embed)
    store.add(Demo("t1", "aaa", "codeA"))
    store.add(Demo("t2", "aab", "codeB"))
    out = store.recall("aaa", k=2, exclude_task_id="t1")
    assert all(d.task_id != "t1" for d in out)

def test_recall_k_caps_results():
    store = LocalTrajectoryStore(embed_fn=_fake_embed)
    for i in range(5):
        store.add(Demo(f"t{i}", "a" * (i + 1), f"c{i}"))
    assert len(store.recall("aaa", k=3)) == 3
