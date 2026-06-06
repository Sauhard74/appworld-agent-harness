"""Lightweight live status for a running AppWorld experiment.

Incremental + cached: only evaluates NEW completed tasks each call (one at a time)
and caches verdicts to .cache/<exp>_status.json, so memory stays bounded and we
never re-evaluate the whole split (which OOMs).

Usage: python scripts/live_status.py <experiment_name> [total]
"""
import json
import os
import sys

EXP = sys.argv[1] if len(sys.argv) > 1 else "team_tn_tex_gpt55"
TOTAL = int(sys.argv[2]) if len(sys.argv) > 2 else 168

BASE = f"experiments/outputs/{EXP}/tasks"
CACHE = f".cache/{EXP}_status.json"
os.makedirs(".cache", exist_ok=True)


def load_cache():
    try:
        return json.load(open(CACHE))
    except Exception:
        return {}


def main():
    cache = load_cache()
    ids = sorted(os.listdir(BASE)) if os.path.isdir(BASE) else []
    new = [t for t in ids if t not in cache]
    if new:
        from appworld import evaluate_task
        for t in new:
            try:
                r = evaluate_task(task_id=t, experiment_name=EXP)
                cache[t] = bool(getattr(r, "success", False))
            except Exception:
                cache[t] = None  # not yet evaluable / errored; retry next cycle
        # drop None entries so they retry next time
        json.dump({k: v for k, v in cache.items() if v is not None}, open(CACHE, "w"))
        cache = load_cache()
    scored = [v for v in cache.values() if v is not None]
    ok = sum(1 for v in scored if v)
    running = os.popen("pgrep -f 'python agent.py' | wc -l").read().strip() != "0"
    pct = 100 * ok / max(len(scored), 1)
    print(f"📊 {EXP}: {len(ids)}/{TOTAL} run | {ok}/{len(scored)} success = {pct:.1f}% TGC "
          f"| {'RUNNING' if running else 'STOPPED'}")


if __name__ == "__main__":
    main()
