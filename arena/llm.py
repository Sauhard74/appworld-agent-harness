import time
from arena import config

USAGE = {"prompt": 0, "completion": 0, "calls": 0}

_client = None
def _get_client():
    global _client
    if _client is None:
        from openai import OpenAI
        kwargs = {}
        if config.OPENAI_BASE_URL:
            kwargs["base_url"] = config.OPENAI_BASE_URL
        _client = OpenAI(**kwargs)  # base_url + OPENAI_API_KEY from env
    return _client

def _create(**kwargs):
    return _get_client().responses.create(**kwargs)

def call_llm(messages, system=None, model=None, max_output_tokens=None, retries=4):
    model = model or config.MODEL
    budget = max_output_tokens or config.MAX_OUTPUT_TOKENS
    last = None
    for attempt in range(retries):
        params = {"model": model, "input": list(messages), "max_output_tokens": budget}
        if system:
            params["instructions"] = system
        try:
            resp = _create(**params)
            u = getattr(resp, "usage", None)
            if u:
                USAGE["prompt"] += getattr(u, "input_tokens", 0)
                USAGE["completion"] += getattr(u, "output_tokens", 0)
            USAGE["calls"] += 1
            text = getattr(resp, "output_text", "") or ""
            if not text and getattr(resp, "status", "") == "incomplete":
                budget = min(budget * 2, 16000)          # reasoning ate the budget; grow & retry
                continue
            return text
        except Exception as e:
            last = e
            time.sleep(min(2 ** attempt, 20))            # backoff on rate/transient
    raise RuntimeError(f"LLM call failed after {retries} attempts: {last}")
