"""Tests for the LLM wrapper. The default graded path is "chat" (Groq)."""
import arena.llm as llm
from arena import config


class _ChatResp:
    def __init__(self, text):
        msg = type("M", (), {"content": text})
        self.choices = [type("C", (), {"message": msg})]
        self.usage = type("U", (), {"prompt_tokens": 5, "completion_tokens": 7})


class _RespResp:
    def __init__(self, text, status="completed"):
        self.output_text = text
        self.status = status
        self.usage = type("U", (), {"input_tokens": 5, "output_tokens": 7})


def test_chat_returns_text(monkeypatch):
    monkeypatch.setattr(config, "LLM_API", "chat")
    monkeypatch.setattr(llm, "_create_chat", lambda **kw: _ChatResp("hello"))
    assert llm.call_llm([{"role": "user", "content": "hi"}], system="sys") == "hello"


def test_chat_passes_system_as_message(monkeypatch):
    monkeypatch.setattr(config, "LLM_API", "chat")
    seen = {}
    def capture(**kw):
        seen.update(kw); return _ChatResp("ok")
    monkeypatch.setattr(llm, "_create_chat", capture)
    llm.call_llm([{"role": "user", "content": "hi"}], system="SYS")
    assert seen["messages"][0] == {"role": "system", "content": "SYS"}
    assert seen["messages"][1] == {"role": "user", "content": "hi"}


def test_responses_path_retries_on_incomplete_empty(monkeypatch):
    monkeypatch.setattr(config, "LLM_API", "responses")
    calls = {"n": 0}
    def flaky(**kw):
        calls["n"] += 1
        return _RespResp("", status="incomplete") if calls["n"] == 1 else _RespResp("done")
    monkeypatch.setattr(llm, "_create", flaky)
    assert llm.call_llm([{"role": "user", "content": "hi"}], system="s") == "done"
    assert calls["n"] == 2
