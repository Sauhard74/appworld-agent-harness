from arena.splits import held_out_slice
def test_slice_deterministic_and_disjoint():
    ids = [f"t{i}" for i in range(20)]
    a = held_out_slice(ids, frac=0.3)
    b = held_out_slice(ids, frac=0.3)
    assert a == b                       # deterministic
    assert len(a) == 6
    tune = [x for x in ids if x not in set(a)]
    assert set(a).isdisjoint(tune)      # disjoint from tuning set
