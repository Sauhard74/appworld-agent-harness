from arena import config
from arena.utils import extract_code, truncate_obs
from arena.prompt import SYSTEM_PROMPT, build_initial_messages
from arena.llm import call_llm as _default_call_llm

_ERR_MARKERS = ("Traceback", "Error", "Exception")

_ERROR_NUDGE = ("\n\nThat raised an error. First diagnose the root cause in a "
                "one-line comment, then output the corrected single code block.")

# Injected once after the agent first calls complete_task. Targets the dominant
# weak-model failure: confidently submitting a wrong/empty answer or making stray
# writes. The agent can re-call complete_task (it overwrites) to fix.
_VERIFY_PROMPT = (
    "\n\nSTOP — verify before we finalize. In ONE code block, sanity-check your work:\n"
    "1. Re-read/print the answer or the records you changed.\n"
    "2. If it's a question: is the answer NON-EMPTY and in the EXACT requested format "
    "(separators, spacing, count, order)? An empty/zero/None result almost always means "
    "a filter matched nothing — print the distinct values you filtered on and recheck.\n"
    "3. Did you change ONLY what the task required (no stray writes to other apps/records)?\n"
    "If anything is wrong, FIX it and call apis.supervisor.complete_task(answer=...) again "
    "(it overwrites). If everything is correct, print exactly DONE_VERIFIED."
)

# How many extra turns the agent gets to fix things during verification.
_VERIFY_TURNS = 4


def _looks_like_error(obs: str) -> bool:
    return any(m in obs for m in _ERR_MARKERS)


def solve(env, demos, call_llm=None, max_turns=None, verify=None):
    call_llm = call_llm or (lambda messages, system: _default_call_llm(messages, system=system))
    max_turns = max_turns or config.MAX_TURNS
    if verify is None:
        verify = config.VERIFY
    messages = build_initial_messages(env, demos)
    trajectory = []
    phase = "solve"
    verify_left = _VERIFY_TURNS
    for turn in range(1, max_turns + 1):
        reply = call_llm(messages, system=SYSTEM_PROMPT)
        code = extract_code(reply)
        try:
            obs = str(env.execute(code))
        except Exception as e:
            obs = f"Runtime error executing your code: {e!r}"
        obs_t = truncate_obs(obs, config.OBS_HEAD, config.OBS_TAIL)
        trajectory.append({"code": code, "obs": obs_t})
        done = env.done()

        user_msg = f"Execution output:\n{obs_t}"
        if _looks_like_error(obs):
            user_msg += _ERROR_NUDGE
        # First completion -> enter verification phase (one combined message).
        if done and verify and phase == "solve":
            phase = "verify"
            user_msg += _VERIFY_PROMPT
            messages.append({"role": "assistant", "content": reply})
            messages.append({"role": "user", "content": user_msg})
            continue

        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": user_msg})

        if done:
            if phase == "verify":
                if "DONE_VERIFIED" in reply or verify_left <= 0:
                    return {"completed": True, "turns": turn, "trajectory": trajectory}
                verify_left -= 1
                continue
            return {"completed": True, "turns": turn, "trajectory": trajectory}
    return {"completed": env.done(), "turns": max_turns, "trajectory": trajectory}
