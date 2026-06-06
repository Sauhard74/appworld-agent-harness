import json, os
from arena.demos import load_gold_demos

def test_load_gold_demos_reads_instruction_and_body(tmp_path):
    t = tmp_path / "tasks" / "x1"
    (t / "ground_truth").mkdir(parents=True)
    (t / "specs.json").write_text(json.dumps({"instruction": "do thing"}))
    (t / "ground_truth" / "solution.py").write_text("# Canary String: zzz\ncode_here()\n")
    demos = load_gold_demos(["x1"], data_dir=str(tmp_path))
    assert len(demos) == 1
    assert demos[0].instruction == "do thing"
    assert "code_here()" in demos[0].body
    assert "Canary" not in demos[0].body  # header stripped
