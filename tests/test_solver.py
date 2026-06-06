from arena.solver import solve

class FakeEnv:
    instruction = "do it"
    supervisor = {}
    def __init__(self, complete_after=1):
        self.calls = []; self.n = 0; self.complete_after = complete_after
    def execute(self, code):
        self.calls.append(code); self.n += 1
        return "ok" if self.n >= self.complete_after else "partial"
    def done(self):
        return self.n >= self.complete_after

def test_solver_stops_when_done():
    env = FakeEnv(complete_after=1)
    llm = lambda messages, system: "```python\nprint(1)\n```"
    res = solve(env, [], call_llm=llm, max_turns=5)
    assert res["completed"] is True and res["turns"] == 1

def test_solver_respects_max_turns():
    env = FakeEnv(complete_after=99)
    llm = lambda messages, system: "```python\nprint(1)\n```"
    res = solve(env, [], call_llm=llm, max_turns=3)
    assert res["completed"] is False and res["turns"] == 3

def test_solver_adds_reflection_on_error():
    env = FakeEnv(complete_after=99)
    seen = {"reflect": False}
    def llm(messages, system):
        if any("diagnose" in m["content"].lower() for m in messages):
            seen["reflect"] = True
        return "```python\nbad\n```"
    class ErrEnv(FakeEnv):
        def execute(self, code): self.n += 1; return "Traceback: ValueError"
        def done(self): return False
    solve(ErrEnv(complete_after=99), [], call_llm=llm, max_turns=2)
    assert seen["reflect"] is True
