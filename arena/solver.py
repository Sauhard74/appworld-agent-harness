from arena import config
from arena.utils import extract_code, truncate_obs
from arena.prompt import SYSTEM_PROMPT, build_initial_messages
from arena.llm import call_llm as _default_call_llm

_ERR_MARKERS = ("Traceback", "Error", "Exception")

def _looks_like_error(obs: str) -> bool:
    return any(m in obs for m in _ERR_MARKERS)

def solve(env, demos, call_llm=None, max_turns=None):
    call_llm = call_llm or (lambda messages, system: _default_call_llm(messages, system=system))
    max_turns = max_turns or config.MAX_TURNS
    messages = build_initial_messages(env, demos)
    trajectory = []
    for turn in range(1, max_turns + 1):
        reply = call_llm(messages, system=SYSTEM_PROMPT)
        code = extract_code(reply)
        try:
            obs = str(env.execute(code))
        except Exception as e:
            obs = f"Runtime error executing your code: {e!r}"
        obs_t = truncate_obs(obs, config.OBS_HEAD, config.OBS_TAIL)
        trajectory.append({"code": code, "obs": obs_t})
        messages.append({"role": "assistant", "content": reply})
        user_msg = f"Execution output:\n{obs_t}"
        if _looks_like_error(obs):
            user_msg += ("\n\nThat raised an error. First diagnose the root cause in a "
                         "one-line comment, then output the corrected single code block.")
        messages.append({"role": "user", "content": user_msg})
        if env.done():
            return {"completed": True, "turns": turn, "trajectory": trajectory}
    return {"completed": False, "turns": max_turns, "trajectory": trajectory}
