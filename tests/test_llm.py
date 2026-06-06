import arena.llm as llm

class _Resp:
    def __init__(self, text, status="completed"):
        self.output_text = text
        self.status = status
        self.usage = type("U", (), {"input_tokens": 5, "output_tokens": 7})

def test_call_llm_returns_text(monkeypatch):
    monkeypatch.setattr(llm, "_create", lambda **kw: _Resp("hello"))
    out = llm.call_llm([{"role": "user", "content": "hi"}], system="sys")
    assert out == "hello"

def test_call_llm_retries_on_incomplete_empty(monkeypatch):
    calls = {"n": 0}
    def flaky(**kw):
        calls["n"] += 1
        if calls["n"] == 1:
            return _Resp("", status="incomplete")     # reasoning ate the budget
        return _Resp("done")
    monkeypatch.setattr(llm, "_create", flaky)
    out = llm.call_llm([{"role": "user", "content": "hi"}], system="s")
    assert out == "done" and calls["n"] == 2

def test_call_llm_passes_instructions_and_input(monkeypatch):
    seen = {}
    def capture(**kw):
        seen.update(kw); return _Resp("ok")
    monkeypatch.setattr(llm, "_create", capture)
    llm.call_llm([{"role": "user", "content": "hi"}], system="SYS")
    assert seen["instructions"] == "SYS"
    assert seen["input"] == [{"role": "user", "content": "hi"}]
