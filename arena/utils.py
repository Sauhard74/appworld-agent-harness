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

def trim_messages(messages, max_pairs):
    """Bound context: keep messages[0] (task+demos) + the most recent max_pairs
    turn-pairs. A turn-pair is one assistant msg + its following user msg.

    If there are at most max_pairs pairs after messages[0], return the list
    unchanged. Otherwise drop the oldest middle pairs and insert ONE marker user
    message before the kept recent pairs so the model knows turns were dropped.
    """
    if not messages:
        return messages
    head, rest = messages[:1], messages[1:]
    n_pairs = len(rest) // 2
    if n_pairs <= max_pairs:
        return messages
    keep = rest[-(max_pairs * 2):] if max_pairs > 0 else rest[len(rest):]
    dropped = n_pairs - max_pairs
    marker = {"role": "user",
              "content": f"[... {dropped} earlier turns omitted to save context ...]"}
    return head + [marker] + keep
