import os, time
from arena import config
from arena.env_adapter import AppWorldEnv
from arena.solver import solve
from arena.demos import build_seeded_store
from arena.llm import USAGE

def _already_done(task_id) -> bool:
    """Resumability: skip tasks that already produced output for this experiment."""
    p = os.path.join("experiments", "outputs", config.EXPERIMENT, "tasks", task_id)
    return os.path.exists(p)

def main():
    from appworld import load_task_ids
    task_ids = load_task_ids(config.DATASET)
    if config.MAX_TASKS:
        task_ids = task_ids[: config.MAX_TASKS]
    print(f"Building demo store (seed={config.SEED_SPLITS}, backend={config.MEMORY_BACKEND})...")
    store = build_seeded_store(seed_splits=config.SEED_SPLITS, backend=config.MEMORY_BACKEND)
    print(f"Running '{config.EXPERIMENT}' on {len(task_ids)} '{config.DATASET}' tasks with {config.MODEL}")

    completed = 0
    for i, tid in enumerate(task_ids, 1):
        if _already_done(tid):
            print(f"[{i}/{len(task_ids)}] {tid} — skip (already done)"); continue
        demos = store.recall(_instruction_of(tid), k=config.K_DEMOS, exclude_task_id=tid)
        t0 = time.time()
        try:
            with AppWorldEnv(tid, config.EXPERIMENT) as env:
                res = solve(env, demos)
            completed += int(res["completed"])
            print(f"[{i}/{len(task_ids)}] {tid} — {'✓' if res['completed'] else '✗'} "
                  f"{res['turns']}t {time.time()-t0:.0f}s")
        except Exception as e:
            print(f"[{i}/{len(task_ids)}] {tid} — ! error: {e}")
    print(f"\nLocal-completed {completed}/{len(task_ids)}. "
          f"Tokens: {USAGE['prompt']}p/{USAGE['completion']}c in {USAGE['calls']} calls.")
    print(f"Outputs: ./experiments/outputs/{config.EXPERIMENT}/  → run `appworld evaluate {config.EXPERIMENT} {config.DATASET}`")

def _instruction_of(task_id):
    import json
    return json.load(open(os.path.join(config.DATA_DIR, "tasks", task_id, "specs.json")))["instruction"]

if __name__ == "__main__":
    main()
