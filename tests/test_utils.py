from arena.utils import extract_code, truncate_obs

def test_extract_code_fenced():
    txt = "thinking...\n```python\nprint(1)\n```\ntrailing"
    assert extract_code(txt) == "print(1)"

def test_extract_code_last_block_wins():
    txt = "```python\nx=1\n```\nthen\n```python\nx=2\n```"
    assert extract_code(txt) == "x=2"

def test_extract_code_no_fence_returns_stripped():
    assert extract_code("  print(1)  ") == "print(1)"

def test_truncate_obs_short_passthrough():
    assert truncate_obs("hello", 100, 100) == "hello"

def test_truncate_obs_keeps_head_and_tail():
    s = "A" * 50 + "B" * 50
    out = truncate_obs(s, 10, 10)
    assert out.startswith("AAAAAAAAAA")
    assert out.rstrip().endswith("BBBBBBBBBB")
    assert "truncated" in out

def test_truncate_obs_preserves_traceback_tail():
    s = "noise\n" * 1000 + "Traceback (most recent call last):\nValueError: boom"
    out = truncate_obs(s, 50, 200)
    assert "ValueError: boom" in out
