import re

_FENCE = re.compile(r"```(?:python)?\s*\n(.*?)```", re.S)

def extract_code(text: str) -> str:
    """Return the LAST fenced python block; fall back to stripped text."""
    blocks = _FENCE.findall(text)
    if blocks:
        return blocks[-1].strip()
    return text.strip()

def truncate_obs(obs: str, head: int, tail: int) -> str:
    """Keep head + tail chars; tail bias preserves tracebacks/final values."""
    obs = str(obs)
    if len(obs) <= head + tail:
        return obs
    omitted = len(obs) - head - tail
    return f"{obs[:head]}\n...[{omitted} chars truncated]...\n{obs[-tail:]}"
