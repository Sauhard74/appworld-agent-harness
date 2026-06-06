from arena.utils import extract_code, truncate_obs, trim_messages, has_code_block

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

def _convo(n_pairs):
    # messages[0] = initial user task; then n_pairs of (assistant, user).
    msgs = [{"role": "user", "content": "TASK+DEMOS"}]
    for i in range(n_pairs):
        msgs.append({"role": "assistant", "content": f"a{i}"})
        msgs.append({"role": "user", "content": f"u{i}"})
    return msgs

def test_trim_messages_short_unchanged():
    msgs = _convo(3)
    out = trim_messages(msgs, 16)
    assert out == msgs

def test_trim_messages_long_keeps_first_and_last_pairs():
    msgs = _convo(20)
    out = trim_messages(msgs, 5)
    assert out[0] == {"role": "user", "content": "TASK+DEMOS"}
    # marker inserted once in the gap
    markers = [m for m in out if m["role"] == "user" and "omitted" in m["content"]]
    assert len(markers) == 1
    # exactly the last 5 pairs (10 messages) kept after marker
    kept = out[2:]
    assert kept == _convo(20)[-10:]
    # structure: first + marker + 10 = 12 messages
    assert len(out) == 12

def test_has_code_block_detects_fence():
    assert has_code_block("blah\n```python\nx=1\n```") is True
    assert has_code_block("```\nx=1\n```") is True

def test_has_code_block_false_for_prose():
    assert has_code_block("just talking, no fence here") is False

def test_trim_messages_preserves_most_recent_user():
    msgs = _convo(20)
    out = trim_messages(msgs, 5)
    assert out[-1] == {"role": "user", "content": "u19"}
