from arena import config
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
    res = solve(env, [], call_llm=llm, max_turns=5, verify=False)
    assert res["completed"] is True and res["turns"] == 1

def test_solver_respects_max_turns():
    env = FakeEnv(complete_after=99)
    llm = lambda messages, system: "```python\nprint(1)\n```"
    res = solve(env, [], call_llm=llm, max_turns=3, verify=False)
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
    solve(ErrEnv(complete_after=99), [], call_llm=llm, max_turns=2, verify=False)
    assert seen["reflect"] is True

def test_verify_injects_check_and_accepts_on_confirmation():
    # Completes on turn 1; verifier injects a check; agent confirms with DONE_VERIFIED.
    env = FakeEnv(complete_after=1)
    seen = {"verify_prompt": False}
    def llm(messages, system):
        if any("DONE_VERIFIED" in m["content"] for m in messages):
            seen["verify_prompt"] = True
            return "```python\nprint('DONE_VERIFIED')\n```"
        return "```python\napis.supervisor.complete_task(answer='x')\n```"
    res = solve(env, [], call_llm=llm, max_turns=10, verify=True)
    assert seen["verify_prompt"] is True          # verifier turn happened
    assert res["completed"] is True
    assert res["turns"] == 2                       # solve turn + one verify turn

def test_no_code_block_skips_execution_and_nudges():
    env = FakeEnv(complete_after=99)
    seen = {"nudge": False}
    def llm(messages, system):
        if any("no python code block" in m["content"].lower() for m in messages):
            seen["nudge"] = True
        return "I think we should look at the docs first."  # prose, no fence
    solve(env, [], call_llm=llm, max_turns=2, verify=False)
    assert seen["nudge"] is True
    assert env.calls == []  # env.execute never called for prose-only turns

def test_repeated_identical_code_triggers_repeat_nudge():
    env = FakeEnv(complete_after=99)
    seen = {"repeat": False}
    def llm(messages, system):
        if any("identical code to last turn" in m["content"].lower() for m in messages):
            seen["repeat"] = True
        return "```python\nprint(1)\n```"  # same code every turn
    solve(env, [], call_llm=llm, max_turns=3, verify=False)
    assert seen["repeat"] is True
    assert len(env.calls) >= 2  # still executes each turn

def test_verify_lets_agent_fix_then_finish():
    # Agent keeps "completing" but only confirms after a couple of verify turns.
    env = FakeEnv(complete_after=1)
    calls = {"n": 0}
    def llm(messages, system):
        in_verify = any("STOP — verify" in m["content"] for m in messages)
        calls["n"] += 1
        if in_verify and calls["n"] >= 4:
            return "```python\nprint('DONE_VERIFIED')\n```"
        return "```python\napis.supervisor.complete_task(answer='x')\n```"
    res = solve(env, [], call_llm=llm, max_turns=10, verify=True)
    assert res["completed"] is True


# --- rolling-summary context compaction ---------------------------------

class _CodeEnv(FakeEnv):
    """Each execute returns a bulky distinct observation; never completes."""
    def execute(self, code):
        self.calls.append(code); self.n += 1
        return f"Execution output: BIG_OBS_{self.n} " + ("x" * 200)
    def done(self):
        return False


def test_summarize_folds_old_observations_keeps_code_verbatim(monkeypatch):
    monkeypatch.setattr(config, "HISTORY_MODE", "summarize")
    monkeypatch.setattr(config, "MAX_HISTORY_TURNS", 2)
    env = _CodeEnv(complete_after=99)
    sent = {"last": None}

    def llm(messages, system):
        sent["last"] = messages
        # emit a distinct code block per turn so we can find it verbatim
        return f"```python\nprint('CODE_{env.n}')\n```"

    solve(env, [], call_llm=llm, max_turns=6, verify=False,
          summarize_fn=lambda t: "SUMMARY")

    msgs = sent["last"]
    # messages[0] (task+demos) kept verbatim and first.
    assert msgs[0]["role"] == "user" and "YOUR TASK" in msgs[0]["content"]
    # exactly one rolling summary message follows messages[0].
    summary = msgs[1]
    assert summary["role"] == "user"
    assert "Summary of earlier turns" in summary["content"]
    # old turns' CODE is kept verbatim inside the summary (nothing dropped).
    assert "print('CODE_1')" in summary["content"]
    # old OBSERVATIONS are condensed to SUMMARY (not the raw BIG_OBS).
    assert "SUMMARY" in summary["content"]
    assert "BIG_OBS_1" not in summary["content"]
    # recent pairs stay fully verbatim (latest observation present).
    tail = "".join(m["content"] for m in msgs[2:])
    assert "BIG_OBS" in tail


def test_summarize_keeps_recent_pairs_verbatim(monkeypatch):
    monkeypatch.setattr(config, "HISTORY_MODE", "summarize")
    monkeypatch.setattr(config, "MAX_HISTORY_TURNS", 2)
    env = _CodeEnv(complete_after=99)
    sent = {"last": None}
    def llm(messages, system):
        sent["last"] = messages
        return f"```python\nprint('CODE_{env.n}')\n```"
    solve(env, [], call_llm=llm, max_turns=6, verify=False,
          summarize_fn=lambda t: "SUMMARY")
    msgs = sent["last"]
    # most-recent MAX_HISTORY_TURNS pairs kept verbatim after the summary.
    recent = msgs[2:]
    assert len(recent) == 2 * 2  # 2 pairs of (assistant, user)
    # their raw observations are present verbatim, not summarized.
    assert any("BIG_OBS" in m["content"] for m in recent if m["role"] == "user")


def test_full_mode_passes_everything_through(monkeypatch):
    monkeypatch.setattr(config, "HISTORY_MODE", "full")
    monkeypatch.setattr(config, "MAX_HISTORY_TURNS", 2)
    env = _CodeEnv(complete_after=99)
    sent = {"last": None}
    def llm(messages, system):
        sent["last"] = messages
        return f"```python\nprint('CODE_{env.n}')\n```"
    solve(env, [], call_llm=llm, max_turns=6, verify=False,
          summarize_fn=lambda t: "SUMMARY")
    msgs = sent["last"]
    # no summary message; every raw observation present verbatim.
    assert all("Summary of earlier turns" not in m["content"] for m in msgs)
    assert "BIG_OBS_1" in "".join(m["content"] for m in msgs)


def test_summarize_no_fold_when_under_threshold(monkeypatch):
    monkeypatch.setattr(config, "HISTORY_MODE", "summarize")
    monkeypatch.setattr(config, "MAX_HISTORY_TURNS", 10)
    env = _CodeEnv(complete_after=99)
    sent = {"last": None}
    def llm(messages, system):
        sent["last"] = messages
        return f"```python\nprint('CODE_{env.n}')\n```"
    solve(env, [], call_llm=llm, max_turns=3, verify=False,
          summarize_fn=lambda t: "SUMMARY")
    msgs = sent["last"]
    # below threshold: nothing folded, no summary message inserted.
    assert all("Summary of earlier turns" not in m["content"] for m in msgs)
