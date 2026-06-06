from arena import config
from arena.utils import extract_code, truncate_obs, has_code_block
from arena.prompt import SYSTEM_PROMPT, build_initial_messages
from arena.llm import call_llm as _default_call_llm

# Default observation-compactor: asks the graded LLM to condense one tool output
# to 1-2 lines, preserving concrete facts. Tests inject a fake (no network).
_SUMMARIZE_SYSTEM = "You compress tool outputs."
_SUMMARIZE_INSTR = (
    "Condense this tool output to 1-2 lines, preserving concrete facts "
    "(ids, names, counts, errors). Do NOT add commentary:\n\n"
)


def _default_summarize(text: str) -> str:
    return _default_call_llm(
        [{"role": "user", "content": _SUMMARIZE_INSTR + text[:6000]}],
        system=_SUMMARIZE_SYSTEM,
    )

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
    "3. COMPLETENESS: re-fetch the relevant list across ALL pages (fetch_all) and confirm "
    "you handled EVERY matching item, not just page one. Missing a single item fails.\n"
    "4. Did you change ONLY what the task required (no stray writes to other apps/records)?\n"
    "If anything is wrong, FIX it and call apis.supervisor.complete_task(answer=...) again "
    "(it overwrites). If everything is correct, print exactly DONE_VERIFIED."
)

# How many extra turns the agent gets to fix things during verification.
_VERIFY_TURNS = 4

# Weak models sometimes reply with prose and no code, or loop on identical code.
_NO_CODE_NUDGE = ("Your reply had no python code block. Respond with EXACTLY ONE "
                  "```python code block.")
_REPEAT_NUDGE = ("\n\nYou ran identical code to last turn; it will behave the same. "
                 "Change approach: re-read the relevant API doc or change inputs.")


def _looks_like_error(obs: str) -> bool:
    return any(m in obs for m in _ERR_MARKERS)


def _compact(messages, summary_parts, folded_upto, summarize_fn):
    """Build the message list to send under HISTORY_MODE == "summarize".

    Never drops a turn. Folds OLD pairs (beyond the most-recent
    MAX_HISTORY_TURNS) into a rolling summary: each assistant CODE is kept
    VERBATIM; only the bulky user OBSERVATION is condensed via summarize_fn.
    messages[0] (task+demos) and the recent pairs stay fully verbatim. Each
    observation is summarized at most once (folded_upto advances). Returns
    (messages_to_send, new_folded_upto).
    """
    total_pairs = (len(messages) - 1) // 2
    target = max(0, total_pairs - config.MAX_HISTORY_TURNS)
    while folded_upto < target:
        a = messages[1 + 2 * folded_upto]   # assistant (code) -> keep verbatim
        u = messages[2 + 2 * folded_upto]   # user (observation) -> summarize
        summary_parts.append(
            "[code]\n" + extract_code(a["content"]) +
            "\n[result] " + summarize_fn(u["content"])
        )
        folded_upto += 1
    messages_to_send = [messages[0]]
    if summary_parts:
        messages_to_send.append({
            "role": "user",
            "content": ("Summary of earlier turns (code kept verbatim, "
                        "outputs condensed):\n" + "\n".join(summary_parts)),
        })
    messages_to_send += messages[1 + 2 * folded_upto:]
    return messages_to_send, folded_upto


def solve(env, demos, call_llm=None, max_turns=None, verify=None, summarize_fn=None):
    call_llm = call_llm or (lambda messages, system: _default_call_llm(messages, system=system))
    summarize_fn = summarize_fn or _default_summarize
    max_turns = max_turns or config.MAX_TURNS
    if verify is None:
        verify = config.VERIFY
    messages = build_initial_messages(env, demos)
    trajectory = []
    phase = "solve"
    verify_left = _VERIFY_TURNS
    prev_code = None
    summary_parts = []   # rolling, folded-once summary entries for old pairs
    folded_upto = 0      # number of old pairs already folded into summary_parts
    for turn in range(1, max_turns + 1):
        if config.HISTORY_MODE == "summarize":
            messages_to_send, folded_upto = _compact(
                messages, summary_parts, folded_upto, summarize_fn)
        else:
            messages_to_send = messages
        reply = call_llm(messages_to_send, system=SYSTEM_PROMPT)

        # Weak-model guard: prose with no code block -> don't execute arbitrary
        # text. Nudge for exactly one code block; still consumes a turn.
        if not has_code_block(reply):
            messages.append({"role": "assistant", "content": reply})
            messages.append({"role": "user", "content": _NO_CODE_NUDGE})
            continue

        code = extract_code(reply)
        repeated = code == prev_code
        prev_code = code
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
        if repeated:
            user_msg += _REPEAT_NUDGE
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
