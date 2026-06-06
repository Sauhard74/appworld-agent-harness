from arena.prompt import build_initial_messages, SYSTEM_PROMPT
from arena.memory import Demo

class _Task:
    instruction = "Send $5 to Bob"
    supervisor = {"first_name": "Amy"}

def test_messages_include_task_and_demos():
    msgs = build_initial_messages(_Task(), [Demo("d1", "Send $3 to Al", "PAY_CODE")])
    blob = "\n".join(m["content"] for m in msgs)
    assert "Send $5 to Bob" in blob
    assert "PAY_CODE" in blob
    assert "Send $3 to Al" in blob

def test_system_prompt_mentions_no_stray_writes():
    assert "only" in SYSTEM_PROMPT.lower()

def test_messages_handle_zero_demos():
    msgs = build_initial_messages(_Task(), [])
    assert any("Send $5 to Bob" in m["content"] for m in msgs)
