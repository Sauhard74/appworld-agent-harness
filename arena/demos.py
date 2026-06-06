import json, os
from arena.memory import Demo, LocalTrajectoryStore

def _strip_header(src: str) -> str:
    lines = src.splitlines()
    out = [ln for ln in lines if not ln.strip().startswith("# Canary String")]
    return "\n".join(out).strip()

def load_gold_demos(task_ids, data_dir="data"):
    demos = []
    for tid in task_ids:
        base = os.path.join(data_dir, "tasks", tid)
        spec_p = os.path.join(base, "specs.json")
        sol_p = os.path.join(base, "ground_truth", "solution.py")
        if not (os.path.exists(spec_p) and os.path.exists(sol_p)):
            continue
        instruction = json.load(open(spec_p))["instruction"]
        body = _strip_header(open(sol_p).read())
        demos.append(Demo(task_id=tid, instruction=instruction, body=body))
    return demos

def build_seeded_store(seed_splits=("train", "dev"), data_dir="data", embed_fn=None, backend="local"):
    """Load gold demos from the given splits into the chosen MemoryStore backend.

    backend="local" -> LocalTrajectoryStore (cosine over embeddings)
    backend="tex"   -> TexMemoryStore (Tex semantic retriever, bodies kept locally)
    """
    from appworld import load_task_ids
    if backend == "tex":
        from arena.memory_tex import TexMemoryStore
        store = TexMemoryStore()
    else:
        store = LocalTrajectoryStore(embed_fn=embed_fn)
    all_demos = []
    for split in seed_splits:
        all_demos.extend(load_gold_demos(load_task_ids(split), data_dir=data_dir))
    store.add_many(all_demos)
    return store
