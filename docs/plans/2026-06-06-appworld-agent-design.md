# AppWorld Agent — Design

**Date:** 2026-06-06
**Goal:** Build an autonomous interactive coding agent that maximizes **Task Goal Completion (TGC)** on the AppWorld benchmark, scored on a *hidden* AppWorld split. Stretch target: beat the best scaffold-only leaderboard entry (68.5 TGC on `test_normal`); aim 75–85.

## Context & key facts (reverse-engineered from the repo)

- **Task:** read a natural-language instruction → act by writing Python that calls app APIs, **one code block per turn**, observing `print()` output each step (ReAct code-agent).
- **Scale:** 9 apps, 457 APIs, ~100 simulated people. Splits: `train` 90, `dev` 57, `test_normal` 168, `test_challenge` 417.
- **Difficulty is skewed hard.** Hard tasks chain ~39 API calls / ~90 LOC across multiple apps (e.g. parse roommates' phone messages → update Spotify playlist).
- **The eval is strict (the central insight).** `evaluation.py` requires *every* assertion to pass for TGC, and checks **exact DB state**: e.g. `changed_model_names() == {"spotify.PlaylistSong"}` — **any unintended write to the wrong table fails the whole task**, plus exact added/removed record diffs. ⇒ precision and "no collateral damage" matter as much as completing the main goal.
- **Gold data available for building:** `train` (90) and `dev` (57) ship full, well-commented gold `solution.py`. `test_*` ship none. ⇒ we can seed memory and self-evaluate locally.
- **Leaderboard bar:** RL-trained Qwen3-14B = 86.9 (needs training); IBM CUGA = 73.2; **ReAct + 2 retrieved demos = 68.5** (the big scaffold win, +20 over plain ReAct's 48.8) — all on GPT-4o. We use **OpenAI GPT-5.x**, far stronger.

## Constraints / decisions

- **Brain:** OpenAI GPT-5.x (`gpt-5.5` / `gpt-5.3-codex`), env-configurable; exact id confirmed at first run.
- **Time:** 1–2 days. **Architecture:** A→B incremental.
- **Agnostic scope:** *hidden AppWorld split* — same 9 apps/457 APIs, unseen instructions. So we fully exploit AppWorld *structure* (API docs, general gotchas) but never overfit to specific dev/test_normal *tasks/answers*.
- **Memory:** pluggable `MemoryStore`. Two backends A/B-compared on a held-out slice: `LocalTrajectoryStore` vs `TexMemoryStore` (Tex by MetaCognition). Ship the winner.
- **Demos:** self-distilled (agent's own passing trajectories) + **gold-seeded**; retrieved by **similarity only**, never exact-task lookup.
- **HydraDB bonus:** cheap-only — behind the same `MemoryStore` interface, or skip if Tex covers the memory story.

## Architecture

Single solving process (no multi-agent in phase 1), modular so phase-B bolts on. AppWorld-specific glue is isolated in one adapter; the core loop is benchmark-agnostic. (Light seam, **not** a multi-benchmark plugin framework — YAGNI for an AppWorld-only scope.)

```
config.py     env/model config (MODEL, K_DEMOS, MAX_TURNS, dataset, keys)
llm.py        OpenAI client wrapper: call_llm(), retry/backoff, token accounting
memory.py     MemoryStore interface + LocalTrajectoryStore + TexMemoryStore
demos.py      build/seed demo bank from gold solutions; embed + retrieve top-K
apidocs.py    API-doc index over 457 APIs → retrieve likely-relevant docs per task
prompt.py     general system prompt (principles) + injected AppWorld tips + msg assembly
env_adapter.py thin AppWorld glue: instruction in, execute(code), completion check
solver.py     ReAct loop: execute → observe(truncate) → reflect-on-error → verify → complete
agent.py      orchestration: load tasks, per-task solve, resumable, logging, eval
# phase B
planner.py    advisory step decomposition (non-binding)
verifier.py   pre-completion DB-state self-check
```

## The levers (priority order)

1. **GPT-5.x brain** — swap `anthropic`→`openai`, model env-configurable.
2. **Demo retrieval** *(+20 TGC win)* — retrieve top K=2–3 trajectories most similar to the instruction (cosine over cached OpenAI embeddings; BM25 fallback). Inject as reference examples framed "here's how a *similar* task was solved — adapt to the one-block-per-turn runtime." Source = self-distilled passers, seeded with gold `solution.py`.
3. **AppWorld-tuned prompt tips** (general principles in the system prompt; AppWorld specifics injected as data): discover tools at runtime, read docs before calling, pagination (`find_all_from_pages`), per-app `access_token`, datetime/timezone care, **exact** string matching, json-serializable answers (`answer=None` unless it's a question), and **"mutate only what the task needs — stray writes fail the eval."**
4. **Reflection on error** — on a traceback, inject a focused "diagnose root cause, then fix" nudge before the next turn.
5. **Self-verification before `complete_task`** — agent re-reads the records it changed and confirms they match intent *and nothing extra changed*. Directly targets the strict exact-DB-diff eval. **This is our differentiator.**

## Data flow (per task)

load task → retrieve K demos (+ likely API docs) → *(B: draft advisory plan)* → assemble messages → **ReAct loop** { LLM emits one python block → `world.execute` → smart-truncated observation → reflect if error } → *(B: verifier self-check)* → `complete_task` → stop on `task_completed` or `MAX_TURNS`.

## Anti-overfit guardrails (the user's core concern)

- **Similarity-only retrieval** — a new instruction pulls *analogous* demos; nothing keyed to a specific task/answer. Same generalization properties for both memory backends.
- **Held-out validation slice** — tune prompts/K on train + part of dev; *report and decide* on a dev slice we never tune against. An improvement only counts if it generalizes. This is our overfit early-warning.
- **No per-task special-casing** in code or prompt, ever.
- **Knowledge is retrieved/discovered, not memorized** — API docs discovered at runtime; demos retrieved by similarity.

## Memory A/B (Tex vs local)

`MemoryStore` interface: `remember(task, trajectory, success)` / `recall(instruction, k) -> [demos]`.
- `LocalTrajectoryStore`: cached embeddings + cosine; stores full verbatim code trajectories (best for few-shot demos).
- `TexMemoryStore`: wraps Tex `remember()`/`recall()`. **Risk to measure:** Tex optimizes for conversational memory (Turns→Observations→Entities, bounded prompts) and may compress away the literal code we want as a demo; its LoCoMo/LongMemEval wins don't predict AppWorld trajectory-retrieval quality.
- **Decision rule:** identical agent, swap backend, compare **TGC on the held-out slice**. Ship the winner. (Tex, if it wins, can also satisfy the agnostic/scalable memory story and stand in for the HydraDB bonus.)

## Robustness & cost control

- **Smart observation truncation** (keep head+tail + full tracebacks) so 30–40 turns don't blow context.
- **Encourage batching** — one code block can make many calls; 39-call tasks fit under the turn cap.
- **Resumable runs** — skip tasks already completed in the output folder; re-runs are cheap.
- **Retry/backoff** on transient API errors; per-task try/except (one task never kills the run).
- Cheaper model for dev iteration; strongest model for the final scoring run.

## Phase B (after A scores on dev)

- **Planner** — advisory plan (kept non-binding; rigid PlanExec historically *hurt*: 44.6 < ReAct 48.8).
- **Verifier** — explicit DB-state diff self-check before completion.
- **Self-distilled demo flywheel** — run agent on train+dev, keep *passing* runtime-format trajectories, prefer them over gold (they match the exact interface).
- **HydraDB** (cheap-only) — `MemoryStore` impl for the 🐉 bonus if time permits and Tex hasn't already covered it.

## Testing / eval loop

Iterate on **dev (57)** with local `appworld evaluate $EXP dev`. Fast inner loop on a ~15-task difficulty-spanning subset; full dev at checkpoints; report on the held-out slice. Log per-task pass/fail + failure reason to drive prompt fixes. Final: `test_normal` (168) → self-eval → zip `experiments/outputs/$EXP/` (must include `evaluations/test_normal.json` + `tasks/<id>/dbs/`).

**Success criteria:** beat 68.5 TGC on test_normal; stretch 75–85; held-out slice confirms it generalizes (not dev-overfit).
