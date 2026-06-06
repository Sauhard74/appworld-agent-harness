"""LLM wrapper.

Two backends, switched by config.LLM_API:
  - "chat"      -> OpenAI-compatible chat/completions (Groq Llama 3.3 70B — the
                   MANDATED graded model). client built from GROQ_*.
  - "responses" -> Azure Responses API (gpt-5.5 etc.) for building/experiments only.

Embeddings ALWAYS go through the Azure client (Groq has no embedding API); the
embedding client is exposed as _get_client() so arena.memory keeps working unchanged.
"""
import time
from arena import config

USAGE = {"prompt": 0, "completion": 0, "calls": 0}

_embed_client = None   # Azure (also used by the responses path)
_chat_client = None    # Groq (chat path)


def _get_client():
    """Azure OpenAI-compatible client — used for embeddings and the responses path."""
    global _embed_client
    if _embed_client is None:
        from openai import OpenAI
        kwargs = {}
        if config.OPENAI_BASE_URL:
            kwargs["base_url"] = config.OPENAI_BASE_URL
        _embed_client = OpenAI(**kwargs)  # OPENAI_API_KEY from env
    return _embed_client


def _get_chat_client():
    global _chat_client
    if _chat_client is None:
        from openai import OpenAI
        _chat_client = OpenAI(base_url=config.GROQ_BASE_URL, api_key=config.GROQ_API_KEY)
    return _chat_client


# Thin indirections so tests can monkeypatch them.
def _create_chat(**kwargs):
    return _get_chat_client().chat.completions.create(**kwargs)


def _create(**kwargs):
    return _get_client().responses.create(**kwargs)


def _record_usage(usage, in_attr, out_attr):
    if usage:
        USAGE["prompt"] += getattr(usage, in_attr, 0) or 0
        USAGE["completion"] += getattr(usage, out_attr, 0) or 0
    USAGE["calls"] += 1


def _call_chat(messages, system, model, max_tokens, retries):
    msgs = ([{"role": "system", "content": system}] if system else []) + list(messages)
    last = None
    for attempt in range(retries):
        try:
            resp = _create_chat(model=model, messages=msgs,
                                max_tokens=max_tokens, temperature=config.TEMPERATURE)
            _record_usage(getattr(resp, "usage", None), "prompt_tokens", "completion_tokens")
            return resp.choices[0].message.content or ""
        except Exception as e:
            last = e
            time.sleep(min(2 ** attempt, 20))  # backoff (handles 429 rate limits too)
    raise RuntimeError(f"LLM chat call failed after {retries} attempts: {last}")


def _call_responses(messages, system, model, budget, retries):
    last = None
    for attempt in range(retries):
        params = {"model": model, "input": list(messages), "max_output_tokens": budget}
        if system:
            params["instructions"] = system
        try:
            resp = _create(**params)
            _record_usage(getattr(resp, "usage", None), "input_tokens", "output_tokens")
            text = getattr(resp, "output_text", "") or ""
            if not text and getattr(resp, "status", "") == "incomplete":
                budget = min(budget * 2, 16000)
                continue
            return text
        except Exception as e:
            last = e
            time.sleep(min(2 ** attempt, 20))
    raise RuntimeError(f"LLM responses call failed after {retries} attempts: {last}")


def call_llm(messages, system=None, model=None, max_output_tokens=None, retries=4):
    model = model or config.MODEL
    budget = max_output_tokens or config.MAX_OUTPUT_TOKENS
    if config.LLM_API == "responses":
        return _call_responses(messages, system, model, budget, retries)
    return _call_chat(messages, system, model, budget, retries)
