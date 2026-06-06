import hashlib
def held_out_slice(task_ids, frac=0.3):
    """Deterministic held-out subset (hash-based) we NEVER tune against."""
    def h(x): return int(hashlib.sha1(x.encode()).hexdigest(), 16)
    ordered = sorted(task_ids, key=h)
    n = max(1, round(len(task_ids) * frac))
    return sorted(ordered[:n])
