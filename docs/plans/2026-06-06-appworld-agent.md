# AppWorld Agent Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a retrieval-augmented ReAct coding agent that maximizes Task Goal Completion (TGC) on AppWorld, generalizing to a hidden split (no per-task overfitting).

**Architecture:** A general ReAct core (LLM emits one Python block/turn → execute → observe → reflect-on-error → verify → complete) draws on a pluggable `MemoryStore` (similarity-retrieved demos) and runtime-discovered API docs. AppWorld specifics are isolated in one thin adapter. Phase A ships the core; Phase B adds planner, verifier, the Tex-vs-local memory A/B, and a self-distilled demo flywheel.

**Tech Stack:** Python 3.11, `openai` (Azure Responses API, GPT-5.x brain), `appworld==0.1.x`, `numpy` (cosine), `tex-sdk` (memory A/B), `pytest`. Design doc: `docs/plans/2026-06-06-appworld-agent-design.md`.

**Working dir:** `/Users/sauhardgupta/internship/agent-arena/hack_agent_arena` (a git repo; `.env` is gitignored and already holds the Azure + Tex creds).

**VERIFIED at planning time (live probe of the Azure resource):**
- Brain is **Azure AI Foundry's OpenAI-compatible v1 endpoint, driven via the Responses API.** Base URL `https://metacognitionaiservices.services.ai.azure.com/openai/v1/`. Drive it with a **plain `OpenAI` client** (`OpenAI(base_url=…, api_key=…)`) — Bearer auth is automatic. No AzureOpenAI client, no `api-version` juggling.
- One interface serves all models: `client.responses.create(model, input=[{role,content},…], instructions=<system>, max_output_tokens=…)` → read `resp.output_text`, usage at `resp.usage.{input_tokens,output_tokens}`.
- Working deployments (all on this one endpoint): **`gpt-5.5`** ✅, **`gpt-5.3-codex`** ✅, **`Kimi-K2.6`** ✅. All three are reasoning models that spend output tokens on hidden reasoning → `max_output_tokens` must be generous (≥3000).
- Embeddings: **`text-embedding-3-large`** ✅ (3072-dim) on the same endpoint (`client.embeddings.create`). `3-small`/`ada-002` not deployed.
- `.env` already holds `OPENAI_BASE_URL`, `OPENAI_API_KEY`, `MODEL`, `EMBED_MODEL`.

**Conventions:** new agent code lives in `arena/`. Tests in `tests/`. The original `agent.py` is replaced by a thin entrypoint that calls `arena.agent.main`. Commit after every green step.

---

## Phase 0 — Scaffolding

### Task 0: Project setup, deps, test harness

**Files:**
- Modify: `requirements.txt`
- Create: `arena/__init__.py`, `tests/__init__.py`, `pytest.ini`
- Create: `arena/config.py`

**Step 1: Update requirements.txt**

```
appworld
openai
anthropic
python-dotenv
numpy
tex-sdk
pytest
```

**Step 2: Install**

Run: `source .venv/bin/activate && uv pip install -r requirements.txt`
Expected: installs `openai`, `numpy`, `tex-sdk`, `pytest` (others already present).
If `tex-sdk` fails to resolve, note it and continue — Phase B Task 13 confirms the exact package name from the Tex docs; it is not needed until then.

**Step 3: Create `pytest.ini`**

```ini
[pytest]
testpaths = tests
addopts = -q
```

**Step 4: Create `arena/config.py`**

```python
"""Central config. All knobs are env-overridable; defaults are sane for dev iteration."""
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# --- LLM (OpenAI-compatible v1 endpoint, Responses API) ---
MODEL      = os.environ.get("MODEL", "gpt-5.5")            # gpt-5.5 | gpt-5.3-codex | Kimi-K2.6 (verified)
MAX_OUTPUT_TOKENS = int(os.environ.get("MAX_OUTPUT_TOKENS", "4000"))  # reasoning models need headroom
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL")       # set in .env to the Azure v1 endpoint
EMBED_MODEL = os.environ.get("EMBED_MODEL", "text-embedding-3-large")

# --- AppWorld run ---
DATASET    = os.environ.get("APPWORLD_DATASET", "dev")
EXPERIMENT = os.environ.get("APPWORLD_EXPERIMENT", "team_demo")
MAX_TASKS  = int(os.environ.get("MAX_TASKS", "0"))          # 0 = all
MAX_TURNS  = int(os.environ.get("MAX_INTERACTIONS", "40"))

# --- Retrieval / memory ---
MEMORY_BACKEND = os.environ.get("MEMORY_BACKEND", "local")  # local | tex
K_DEMOS    = int(os.environ.get("K_DEMOS", "2"))
DATA_DIR   = os.environ.get("DATA_DIR", "data")
CACHE_DIR  = os.environ.get("CACHE_DIR", ".cache")

# --- Observation handling ---
OBS_HEAD = int(os.environ.get("OBS_HEAD", "2500"))
OBS_TAIL = int(os.environ.get("OBS_TAIL", "1500"))
```

**Step 5: Commit**

```bash
git add requirements.txt pytest.ini arena/__init__.py tests/__init__.py arena/config.py
git commit -m "chore: scaffold arena package + config"
```

---

## Phase A — Retrieval-augmented ReAct core

### Task 1: Pure utils — code extraction + observation truncation (TDD)

**Files:**
- Create: `arena/utils.py`
- Test: `tests/test_utils.py`

**Step 1: Write failing tests**

```python
# tests/test_utils.py
from arena.utils import extract_code, truncate_obs

def test_extract_code_fenced():
    txt = "thinking...\n```python\nprint(1)\n```\ntrailing"
    assert extract_code(txt) == "print(1)"

def test_extract_code_last_block_wins():
    txt = "```python\nx=1\n```\nthen\n```python\nx=2\n```"
    assert extract_code(txt) == "x=2"

def test_extract_code_no_fence_returns_stripped():
    assert extract_code("  print(1)  ") == "print(1)"

def test_truncate_obs_short_passthrough():
    assert truncate_obs("hello", 100, 100) == "hello"

def test_truncate_obs_keeps_head_and_tail():
    s = "A" * 50 + "B" * 50
    out = truncate_obs(s, 10, 10)
    assert out.startswith("AAAAAAAAAA")
    assert out.rstrip().endswith("BBBBBBBBBB")
    assert "truncated" in out

def test_truncate_obs_preserves_traceback_tail():
    s = "noise\n" * 1000 + "Traceback (most recent call last):\nValueError: boom"
    out = truncate_obs(s, 50, 200)
    assert "ValueError: boom" in out
```

**Step 2: Run, verify fail**

Run: `pytest tests/test_utils.py -v` → FAIL (module missing).

**Step 3: Implement `arena/utils.py`**

```python
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
```

**Step 4: Run, verify pass**

Run: `pytest tests/test_utils.py -v` → PASS.

**Step 5: Commit**

```bash
git add arena/utils.py tests/test_utils.py
git commit -m "feat: code extraction + observation truncation utils"
```

---

### Task 2: LLM wrapper (Responses API over the v1 endpoint)

**Files:**
- Create: `arena/llm.py`
- Test: `tests/test_llm.py`

**Notes for the engineer:** Verified interface — `client.responses.create(model, input=[{role,content},…], instructions=<system>, max_output_tokens=…)`, output at `resp.output_text`, usage at `resp.usage.{input_tokens,output_tokens}`. All three deployments are reasoning models (they burn output tokens on hidden reasoning) so keep `max_output_tokens` ≥ 3000 and, if a turn finishes with empty text and `status="incomplete"`, retry once with a larger budget. Do NOT send `temperature` (these models reject it via this path).

**Step 1: Write failing test (mock the client, no network)**

```python
# tests/test_llm.py
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
```

**Step 2: Run, verify fail.**

**Step 3: Implement `arena/llm.py`**

```python
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
```

**Step 4: Run, verify pass.**

**Step 5: Commit**

```bash
git add arena/llm.py tests/test_llm.py
git commit -m "feat: Responses-API LLM wrapper (v1 endpoint) with reasoning-budget retry + usage tracking"
```

**Step 6: Live smoke (manual)**

Run: `python -c "from arena.llm import call_llm; print(call_llm([{'role':'user','content':'say hi in one word'}]))"`
Expected: a one-word reply (`MODEL=gpt-5.5` from `.env`). Try `MODEL=Kimi-K2.6` and `gpt-5.3-codex` to confirm all three route through the same wrapper.

---

### Task 3: MemoryStore interface + LocalTrajectoryStore (TDD)

**Files:**
- Create: `arena/memory.py`
- Test: `tests/test_memory.py`

**Design:** `Demo = {task_id, instruction, body}` where `body` is the verbatim solution/trajectory text. `recall` ranks by cosine over cached embeddings. Embeddings are injectable so tests run without network.

**Step 1: Write failing tests**

```python
# tests/test_memory.py
import numpy as np
from arena.memory import LocalTrajectoryStore, Demo

def _fake_embed(texts):
    # deterministic 2-d embedding: count of 'a' and 'b'
    return [np.array([t.lower().count("a"), t.lower().count("b")], float) for t in texts]

def test_recall_returns_most_similar():
    store = LocalTrajectoryStore(embed_fn=_fake_embed)
    store.add(Demo("t1", "aaa apples", "codeA"))
    store.add(Demo("t2", "bbb bananas", "codeB"))
    out = store.recall("aaaa", k=1)
    assert len(out) == 1 and out[0].task_id == "t1"

def test_recall_excludes_self_by_task_id():
    store = LocalTrajectoryStore(embed_fn=_fake_embed)
    store.add(Demo("t1", "aaa", "codeA"))
    store.add(Demo("t2", "aab", "codeB"))
    out = store.recall("aaa", k=2, exclude_task_id="t1")
    assert all(d.task_id != "t1" for d in out)

def test_recall_k_caps_results():
    store = LocalTrajectoryStore(embed_fn=_fake_embed)
    for i in range(5):
        store.add(Demo(f"t{i}", "a" * (i + 1), f"c{i}"))
    assert len(store.recall("aaa", k=3)) == 3
```

**Step 2: Run, verify fail.**

**Step 3: Implement `arena/memory.py`**

```python
from dataclasses import dataclass
import numpy as np

@dataclass
class Demo:
    task_id: str
    instruction: str
    body: str

class MemoryStore:
    def add(self, demo: Demo): raise NotImplementedError
    def recall(self, instruction: str, k: int, exclude_task_id=None): raise NotImplementedError

def _openai_embed(texts):
    from arena import config
    from arena.llm import _get_client
    resp = _get_client().embeddings.create(model=config.EMBED_MODEL, input=texts)
    return [np.array(d.embedding, float) for d in resp.data]

class LocalTrajectoryStore(MemoryStore):
    def __init__(self, embed_fn=None):
        self.embed_fn = embed_fn or _openai_embed
        self.demos = []        # list[Demo]
        self.vecs = []         # list[np.ndarray]

    def add(self, demo: Demo):
        self.demos.append(demo)
        self.vecs.append(self.embed_fn([demo.instruction])[0])

    def add_many(self, demos):
        if not demos: return
        vs = self.embed_fn([d.instruction for d in demos])
        self.demos.extend(demos); self.vecs.extend(vs)

    def recall(self, instruction, k, exclude_task_id=None):
        if not self.demos: return []
        q = self.embed_fn([instruction])[0]
        def cos(a, b):
            na, nb = np.linalg.norm(a), np.linalg.norm(b)
            return float(a @ b / (na * nb)) if na and nb else 0.0
        scored = [(cos(q, v), d) for v, d in zip(self.vecs, self.demos)
                  if d.task_id != exclude_task_id]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [d for _, d in scored[:k]]
```

**Step 4: Run, verify pass.**

**Step 5: Commit**

```bash
git add arena/memory.py tests/test_memory.py
git commit -m "feat: MemoryStore interface + LocalTrajectoryStore (cosine recall)"
```

---

### Task 4: Demo bank — seed from gold solutions (TDD where possible)

**Files:**
- Create: `arena/demos.py`
- Test: `tests/test_demos.py`

**Design:** `load_gold_demos(split_task_ids)` reads each task's `specs.json` (instruction) + `ground_truth/solution.py` (body, header stripped). `build_seeded_store(...)` loads train+dev gold demos into a `LocalTrajectoryStore` and caches embeddings to `.cache/` so we embed once.

**Step 1: Write failing test (filesystem fixture, no network)**

```python
# tests/test_demos.py
import json, os
from arena.demos import load_gold_demos

def test_load_gold_demos_reads_instruction_and_body(tmp_path):
    t = tmp_path / "tasks" / "x1"
    (t / "ground_truth").mkdir(parents=True)
    (t / "specs.json").write_text(json.dumps({"instruction": "do thing"}))
    (t / "ground_truth" / "solution.py").write_text("# Canary String: zzz\ncode_here()\n")
    demos = load_gold_demos(["x1"], data_dir=str(tmp_path))
    assert len(demos) == 1
    assert demos[0].instruction == "do thing"
    assert "code_here()" in demos[0].body
    assert "Canary" not in demos[0].body  # header stripped
```

**Step 2: Run, verify fail.**

**Step 3: Implement `arena/demos.py`**

```python
import json, os
from arena.memory import Demo, LocalTrajectoryStore

def _strip_header(src: str) -> str:
    lines = src.splitlines()
    out = [ln for ln in lines if not ln.strip().startswith("# Canary String")]
    return "\n".join(out).strip()

def load_gold_demos(task_ids, data_dir="data"):
    demos = []
    for tid in task_ids:
        base = os.path.join(data_dir, "tasks", tid)
        spec_p = os.path.join(base, "specs.json")
        sol_p = os.path.join(base, "ground_truth", "solution.py")
        if not (os.path.exists(spec_p) and os.path.exists(sol_p)):
            continue
        instruction = json.load(open(spec_p))["instruction"]
        body = _strip_header(open(sol_p).read())
        demos.append(Demo(task_id=tid, instruction=instruction, body=body))
    return demos

def build_seeded_store(seed_splits=("train", "dev"), data_dir="data", embed_fn=None):
    """Load gold demos from the given splits into a LocalTrajectoryStore."""
    from appworld import load_task_ids
    store = LocalTrajectoryStore(embed_fn=embed_fn)
    all_demos = []
    for split in seed_splits:
        all_demos.extend(load_gold_demos(load_task_ids(split), data_dir=data_dir))
    store.add_many(all_demos)
    return store
```

**Step 4: Run, verify pass.**

**Step 5: Commit**

```bash
git add arena/demos.py tests/test_demos.py
git commit -m "feat: gold-solution demo loader + seeded store builder"
```

---

### Task 5: Prompt assembly (TDD)

**Files:**
- Create: `arena/prompt.py`
- Test: `tests/test_prompt.py`

**Design:** `SYSTEM_PROMPT` = general principles + AppWorld tips (injected as content, not hardcoded per-task). `build_initial_messages(task, demos)` returns the message list: demos rendered as reference examples, then the task. Keep demos clearly labeled "reference, adapt to the runtime."

**Step 1: Write failing test**

```python
# tests/test_prompt.py
from arena.prompt import build_initial_messages, SYSTEM_PROMPT
from arena.memory import Demo

class _Task:
    instruction = "Send $5 to Bob"
    supervisor = {"first_name": "Amy"}

def test_messages_include_task_and_demos():
    msgs = build_initial_messages(_Task(), [Demo("d1", "Send $3 to Al", "PAY_CODE")])
    blob = "\n".join(m["content"] for m in msgs)
    assert "Send $5 to Bob" in blob
    assert "PAY_CODE" in blob
    assert "Send $3 to Al" in blob

def test_system_prompt_mentions_no_stray_writes():
    assert "only" in SYSTEM_PROMPT.lower()

def test_messages_handle_zero_demos():
    msgs = build_initial_messages(_Task(), [])
    assert any("Send $5 to Bob" in m["content"] for m in msgs)
```

**Step 2: Run, verify fail.**

**Step 3: Implement `arena/prompt.py`**

```python
SYSTEM_PROMPT = """You are an autonomous coding agent operating inside AppWorld.
You complete the supervisor's task by writing Python that the environment executes.

OUTPUT FORMAT (strict):
- Reply with EXACTLY ONE Python code block per turn and nothing else:
  ```python
  # your code
  ```
- Whatever you print() is returned as the next observation. Inspect before acting.

HOW THE WORLD WORKS:
- `apis` is the ONLY interface to the 9 apps. You do NOT know APIs in advance —
  discover them at runtime:
    print(apis.api_docs.show_app_descriptions())
    print(apis.api_docs.show_api_descriptions(app_name='<app>'))
    print(apis.api_docs.show_api_doc(app_name='<app>', api_name='<api>'))
- Get credentials and log in to obtain access_tokens:
    print(apis.supervisor.show_account_passwords())
- Many list APIs are PAGINATED — loop pages until exhausted; don't assume one page.
- Watch datetimes/timezones, and match strings EXACTLY (names, notes, titles).

DISCIPLINE THAT WINS:
- You may make MANY api calls in one code block — batch discovery, then act. Aim to
  finish well within the turn budget.
- Mutate ONLY what the task requires. Stray writes to unrelated data cause failure.
  Before finishing, re-read what you changed and confirm it matches the request and
  that nothing extra was modified.
- Never invent API names or fields — look them up first.

FINISH:
- When (and only when) the task is fully done and verified:
    apis.supervisor.complete_task(answer=<answer>)   # answer=None unless it's a question
"""

def _render_demo(d, i):
    return (f"--- REFERENCE EXAMPLE {i} (a SIMILAR solved task; adapt the pattern to "
            f"the one-block-per-turn runtime — do not copy verbatim) ---\n"
            f"Task: {d.instruction}\n\nReference solution:\n```python\n{d.body}\n```\n")

def build_initial_messages(task, demos):
    parts = []
    if demos:
        parts.append("Here are reference solutions to similar tasks:\n\n" +
                     "\n".join(_render_demo(d, i + 1) for i, d in enumerate(demos)))
    sup = getattr(task, "supervisor", {})
    parts.append(
        f"Supervisor: {sup}\n\nYOUR TASK: {task.instruction}\n\n"
        "Begin. Remember: exactly one python code block per turn."
    )
    return [{"role": "user", "content": "\n\n".join(parts)}]
```

**Step 4: Run, verify pass.**

**Step 5: Commit**

```bash
git add arena/prompt.py tests/test_prompt.py
git commit -m "feat: system prompt (AppWorld principles) + demo-augmented message assembly"
```

---

### Task 6: Env adapter (thin AppWorld seam)

**Files:**
- Create: `arena/env_adapter.py`
- Test: covered by the live smoke in Task 8 (this is glue over AppWorld; no pure-unit value in mocking the SDK).

**Step 1: Implement `arena/env_adapter.py`**

```python
"""The ONLY AppWorld-aware module besides agent.py orchestration. Keeps the
solver loop benchmark-agnostic: it only needs instruction/supervisor, execute(), done()."""
from appworld import AppWorld

class AppWorldEnv:
    def __init__(self, task_id, experiment_name):
        self._cm = AppWorld(task_id=task_id, experiment_name=experiment_name)
        self.world = None

    def __enter__(self):
        self.world = self._cm.__enter__()
        return self

    def __exit__(self, *a):
        return self._cm.__exit__(*a)

    @property
    def instruction(self):
        return self.world.task.instruction

    @property
    def supervisor(self):
        return self.world.task.supervisor

    def execute(self, code):
        return self.world.execute(code)

    def done(self):
        return self.world.task_completed()
```

**Step 2: Commit**

```bash
git add arena/env_adapter.py
git commit -m "feat: thin AppWorld env adapter (keeps solver loop generic)"
```

---

### Task 7: Solver — ReAct loop with reflection (TDD with a fake env)

**Files:**
- Create: `arena/solver.py`
- Test: `tests/test_solver.py`

**Design:** `solve(env, demos, call_llm=..., max_turns=...)` runs the loop. Reflection: when the observation looks like an error (contains `Traceback`/`Error`), append a focused nudge. Inject is via dependency-injected `call_llm` so tests are deterministic.

**Step 1: Write failing tests**

```python
# tests/test_solver.py
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
```

**Step 2: Run, verify fail.**

**Step 3: Implement `arena/solver.py`**

```python
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
```

**Step 4: Run, verify pass.**

**Step 5: Commit**

```bash
git add arena/solver.py tests/test_solver.py
git commit -m "feat: ReAct solver loop with error-reflection (DI for testing)"
```

---

### Task 8: Orchestration + entrypoint (resumable runs)

**Files:**
- Create: `arena/agent.py`
- Modify: `agent.py` (root) → thin shim calling `arena.agent.main`
- Test: live smoke on 2 dev tasks

**Step 1: Implement `arena/agent.py`**

```python
import os, time
from arena import config
from arena.env_adapter import AppWorldEnv
from arena.solver import solve
from arena.demos import build_seeded_store
from arena.llm import USAGE

def _already_done(task_id) -> bool:
    """Resumability: skip tasks that already produced output for this experiment."""
    p = os.path.join("experiments", "outputs", config.EXPERIMENT, "tasks", task_id)
    return os.path.exists(p)

def main():
    from appworld import load_task_ids
    task_ids = load_task_ids(config.DATASET)
    if config.MAX_TASKS:
        task_ids = task_ids[: config.MAX_TASKS]
    print(f"Building demo store (seed=train+dev, backend={config.MEMORY_BACKEND})...")
    store = build_seeded_store()  # local backend; Task 13 adds tex switch
    print(f"Running '{config.EXPERIMENT}' on {len(task_ids)} '{config.DATASET}' tasks with {config.MODEL}")

    completed = 0
    for i, tid in enumerate(task_ids, 1):
        if _already_done(tid):
            print(f"[{i}/{len(task_ids)}] {tid} — skip (already done)"); continue
        demos = store.recall(_instruction_of(tid), k=config.K_DEMOS, exclude_task_id=tid)
        t0 = time.time()
        try:
            with AppWorldEnv(tid, config.EXPERIMENT) as env:
                res = solve(env, demos)
            completed += int(res["completed"])
            print(f"[{i}/{len(task_ids)}] {tid} — {'✓' if res['completed'] else '✗'} "
                  f"{res['turns']}t {time.time()-t0:.0f}s")
        except Exception as e:
            print(f"[{i}/{len(task_ids)}] {tid} — ! error: {e}")
    print(f"\nLocal-completed {completed}/{len(task_ids)}. "
          f"Tokens: {USAGE['prompt']}p/{USAGE['completion']}c in {USAGE['calls']} calls.")
    print(f"Outputs: ./experiments/outputs/{config.EXPERIMENT}/  → run `appworld evaluate {config.EXPERIMENT} {config.DATASET}`")

def _instruction_of(task_id):
    import json
    return json.load(open(os.path.join(config.DATA_DIR, "tasks", task_id, "specs.json")))["instruction"]

if __name__ == "__main__":
    main()
```

**Step 2: Replace root `agent.py` with a shim**

```python
from arena.agent import main
if __name__ == "__main__":
    main()
```

**Step 3: Live smoke (needs OPENAI_API_KEY + working MODEL id)**

```bash
export APPWORLD_EXPERIMENT=team_<yourname>
export APPWORLD_DATASET=dev MAX_TASKS=2
python agent.py
```
Expected: two tasks run, each prints ✓/✗ and turn count; outputs land in `experiments/outputs/$EXP/`. Fix the MODEL id here if the LLM errors.

**Step 4: Evaluate the smoke**

Run: `appworld evaluate $APPWORLD_EXPERIMENT dev`
Expected: a TGC/SGC number prints (even if low). This proves the full loop + eval works end to end.

**Step 5: Commit**

```bash
git add arena/agent.py agent.py
git commit -m "feat: resumable orchestration + root entrypoint shim"
```

---

### Task 9: Baseline on dev + held-out slice + eval helper

**Files:**
- Create: `arena/splits.py` (deterministic held-out slice)
- Create: `scripts/run_eval.sh`
- Test: `tests/test_splits.py`

**Step 1: Failing test for deterministic slice**

```python
# tests/test_splits.py
from arena.splits import held_out_slice
def test_slice_deterministic_and_disjoint():
    ids = [f"t{i}" for i in range(20)]
    a = held_out_slice(ids, frac=0.3)
    b = held_out_slice(ids, frac=0.3)
    assert a == b                       # deterministic
    assert len(a) == 6
    tune = [x for x in ids if x not in set(a)]
    assert set(a).isdisjoint(tune)      # disjoint from tuning set
```

**Step 2: Implement `arena/splits.py`**

```python
import hashlib
def held_out_slice(task_ids, frac=0.3):
    """Deterministic held-out subset (hash-based) we NEVER tune against."""
    def h(x): return int(hashlib.sha1(x.encode()).hexdigest(), 16)
    ordered = sorted(task_ids, key=h)
    n = max(1, round(len(task_ids) * frac))
    return sorted(ordered[:n])
```

**Step 3: Run test, verify pass.**

**Step 4: Create `scripts/run_eval.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
: "${APPWORLD_EXPERIMENT:?set APPWORLD_EXPERIMENT}"
SPLIT="${1:-dev}"
python agent.py
appworld evaluate "$APPWORLD_EXPERIMENT" "$SPLIT"
```

**Step 5: Establish baseline**

```bash
export APPWORLD_EXPERIMENT=team_<yourname> APPWORLD_DATASET=dev MAX_TASKS=0
bash scripts/run_eval.sh dev
```
Record TGC/SGC in a scratch note. This is the number every later change must beat **on the held-out slice** to count as a real (non-overfit) improvement.

**Step 6: Commit**

```bash
git add arena/splits.py tests/test_splits.py scripts/run_eval.sh
git commit -m "feat: deterministic held-out slice + eval helper; record baseline"
```

**CHECKPOINT:** Phase A core is complete and scoring. Compare baseline TGC to the 48.8 ReAct reference. Proceed to Phase B only after this runs clean.

---

### Task 10: API-doc retrieval injection (measure delta)

**Files:**
- Create: `arena/apidocs.py`
- Modify: `arena/prompt.py` (accept optional `api_hints`), `arena/agent.py` (build hints)
- Test: `tests/test_apidocs.py`

**Design:** Pre-index the 457 API descriptions (app + api name + one-line desc) from `data/api_docs` or via `apis.api_docs`. For a task, retrieve a shortlist of likely-relevant apps/APIs (embedding similarity on the instruction) and inject as a hint block so the agent spends fewer turns discovering. Keep it a *hint*, not a constraint (agent still verifies docs at runtime).

**Steps:** write a test that `select_relevant_apis(instruction, index, k)` returns the closest entries for a fake index/embed; implement; wire an optional `api_hints` section into `build_initial_messages`; A/B on the held-out slice (with vs without hints). **Keep only if it improves held-out TGC** — otherwise revert (avoids context bloat). Commit either the feature or a note that it didn't help.

---

## Phase B — Planner, verifier, memory A/B, flywheel

### Task 11: Verifier — pre-completion self-check

**Files:** Create `arena/verifier.py`; modify `arena/prompt.py`/`arena/solver.py`.

**Design:** Before allowing `complete_task`, inject one extra turn instructing the agent to (a) list the records/entities it created or modified, (b) re-read them, (c) confirm they exactly match the request and that nothing unrelated changed, then either fix or proceed. This directly targets the strict exact-DB-diff eval. Implement as an optional `verify=True` flag in `solve`. Unit-test the message injection with the fake env; **measure TGC delta on the held-out slice**; keep if positive.

Commit: `feat: pre-completion verification turn`.

---

### Task 12: Planner — advisory decomposition

**Files:** Create `arena/planner.py`; modify `arena/prompt.py`/`arena/solver.py`.

**Design:** One upfront LLM call → a short numbered plan from instruction + retrieved demos, injected as advisory context ("a suggested plan; deviate if the world disagrees"). Non-binding (rigid planning historically hurt). Gate behind `PLAN=1`. **Measure held-out TGC; keep only if positive** (expect gains concentrated on hard/multi-app tasks — also check the per-difficulty breakdown).

Commit: `feat: optional advisory planner`.

---

### Task 13: TexMemoryStore + memory A/B

**Files:** Create `arena/memory_tex.py`; modify `arena/agent.py` (`MEMORY_BACKEND` switch); Test `tests/test_memory_tex.py` (mock the Tex client).

**Step 1: Confirm the SDK** — from the Tex docs (`metacognition-fdc534de.mintlify.app`): exact package name, client init with `TEX_API_KEY`, and the `remember()`/`recall()` signatures. Adjust `requirements.txt` if the package name differs from `tex-sdk`.

**Step 2: Implement `TexMemoryStore(MemoryStore)`** — `add()` → `remember()` the (instruction, body); `recall(instruction, k)` → `recall()` and map results back to `Demo(body=...)`. **Critical:** ensure the full code `body` survives round-trip; if Tex summarizes/extracts and drops the literal code, store the code in a metadata/raw field and read it back verbatim. Mock the client in tests to assert the mapping and the verbatim-code guarantee.

**Step 3: A/B** — same agent, run held-out slice twice: `MEMORY_BACKEND=local` vs `MEMORY_BACKEND=tex`. Compare TGC. **Ship the winner**; record both numbers in the scratch note. (If Tex wins, it also covers the agnostic memory story and can stand in for the HydraDB bonus.)

Commit: `feat: Tex memory backend + local-vs-tex A/B result`.

---

### Task 14: Self-distilled demo flywheel

**Files:** Modify `arena/agent.py`; create `scripts/distill_demos.py`.

**Design:** After a run, for every task that **passed local eval**, save its runtime-format trajectory (the one-block-per-turn code, concatenated/cleaned) as a `Demo` to a persistent store file (`.cache/distilled.jsonl`). On subsequent runs, load distilled demos and **prefer them over gold** (they match the exact runtime interface). Only store passers (verified by `appworld evaluate` on the building splits — never on test). Re-run train+dev to build the distilled bank, then re-measure held-out TGC.

Commit: `feat: self-distilled demo flywheel (prefer verified runtime trajectories)`.

---

### Task 15 (optional, bonus): HydraDB memory backend

Only if time remains and Tex hasn't already satisfied the memory story. Implement `HydraMemoryStore(MemoryStore)` behind the same interface (per organizer HydraDB details). Gate behind `MEMORY_BACKEND=hydra`. This earns the 🐉 bonus without touching core logic.

Commit: `feat: optional HydraDB memory backend (bonus)`.

---

### Task 16: Final scoring run + submission package

**Steps:**
1. Pick the winning config (model, K_DEMOS, verify/plan flags, memory backend) per held-out results. Record it.
2. Run the official split:
   ```bash
   export APPWORLD_DATASET=test_normal MAX_TASKS=0 APPWORLD_EXPERIMENT=team_<yourname>
   python agent.py
   ```
   (Resumable — safe to restart if interrupted.)
3. Self-evaluate: `appworld evaluate $APPWORLD_EXPERIMENT test_normal`
4. Verify the output folder contains `evaluations/test_normal.json` and `tasks/<id>/dbs/`.
5. Zip `experiments/outputs/$APPWORLD_EXPERIMENT/` and submit.
6. Commit the final config + the recorded TGC/SGC numbers (not the outputs — `experiments/` is gitignored).

Commit: `chore: record final config and scores`.

---

## Cross-cutting reminders
- **DRY/YAGNI:** don't build the multi-benchmark plugin framework — scope is AppWorld.
- **Every "smart" addition (api hints, planner, verifier, tex) must justify itself on the held-out slice or be reverted.** That is the overfit firewall.
- **Commit after every green step.** Never commit `.env` or `experiments/`.
- **Cost:** iterate on a ~15-task difficulty-spanning dev subset (`MAX_TASKS=15`); full split only at checkpoints and the final run.
