# Methodology — a decision log

This is the *why*. For each technique we explain why we **chose** it; for each tempting
alternative we explain why we **rejected** it. Then the **anti-overfit** protocol — the part
that makes the numbers honest — and how to read the results.

The throughline: AppWorld is **discovery-dependent** (you can't plan what you haven't
explored) and graded by a **strict exact-DB-diff** evaluator (any stray write fails the whole
task). Every decision below is justified against those two facts and against hard
**rate-limit / token** constraints.

---

## Chosen techniques

### 1. Similarity-retrieved gold demos — the primary lever
**Why.** Demo retrieval is the single biggest *scaffold-only* lever on the public AppWorld
leaderboard: plain ReAct ≈ **48.8** TGC → ReAct + retrieved demos ≈ **68.5** TGC, a ~**+20**
swing without any model training. Gold `solution.py` files are the highest-fidelity demos
available (90 train + 57 dev = **147**).
**How.** Retrieve the top `K_DEMOS` (default 2) most similar to the instruction, render them
as *reference examples* framed "adapt the pattern, don't copy verbatim." Retrieval is
**similarity-only** and always excludes the task itself.

### 2. Verifier turn — built for the strict evaluator
**Why.** Two failure modes dominate, and a verifier hits both:
1. The evaluator checks **exact DB state** — a stray write to an unrelated table fails an
   otherwise-correct task. A forced "did you change ONLY what was required?" re-read catches
   collateral damage before it's locked in.
2. Weak models **confidently submit wrong/empty answers** (an empty filter result, a
   mis-formatted string) — observed directly in our own smoke tests.
**How.** After the first `complete_task`, inject a self-check; the agent gets up to 4 turns to
re-call `complete_task` (it **overwrites**) or print `DONE_VERIFIED`. Targeted, bounded cost.

### 3. Pluggable memory with bodies kept local — a *fair* A/B
**Why.** We wanted to compare retrieval *services* (local embeddings vs Tex vs HydraDB)
without confounds, and to integrate HydraDB for the bonus track.
**How.** All backends sit behind one `MemoryStore` interface. External services index **only
the instruction**; the verbatim solution **code stays local** and is reattached at recall.
This guarantees (a) every backend returns *identical* demo bodies → the A/B isolates
retrieval quality alone, and (b) code fidelity — no service can summarize or truncate the
solution.

### 4. Model-agnostic core
**Why.** The graded model changed **three times** (GPT-5.5 → Groq Llama 3.3 70B → Gemini). A
model-agnostic wrapper turned each switch into an env change, not a rewrite — and made the
*harness*, not any one model, the durable contribution.
**How.** `call_llm` dispatches between an OpenAI-compatible `chat` path and an Azure
`responses` path via `LLM_API`; embeddings always use the OpenAI/Azure client.

### 5. TDD, resumable runs, full env-config
**Why.** A 1–2 day hackathon with a moving target needs a fast, trustworthy feedback loop. 44
network-free unit tests let us refactor the solver state machine fearlessly; resumability
makes a 168-task run robust to interruption; env-config makes every feature A/B-able without
code edits.

---

## Rejected alternatives (with rationale)

This rigor matters: knowing what *not* to build is part of the contribution.

### DAG / task-compiler (pre-computed dependency graph)
**Rejected.** AppWorld tasks are **discovery-dependent** — you cannot build the dependency
graph before exploring (e.g. *"update the playlist per my roommates' messages"* requires
reading the messages first). And explicit planning has **historically hurt** on AppWorld:
the leaderboard's PlanExec scaffold (**44.6**) scores *below* plain ReAct (**48.8**). High
risk, token-heavy, evidence against it. ReAct's interleave-think-and-act fits the benchmark.

### External world-graph / state subsystem
**Rejected as redundant.** AppWorld **persists the Python namespace across turns** (verified:
a variable set in turn 1 survives to turn 2), so the agent already holds working state in
plain Python variables. A one-line prompt nudge to keep results in variables captures ~90% of
the value at ~1% of the cost of a bespoke state store.

### Best-of-N / self-consistency
**Rejected on cost.** N× sampling is the worst possible fit under hard rate limits — the
mandated Groq free tier caps at **100,000 tokens per day**. Under that budget a single
disciplined trajectory plus a cheap verifier is the right trade-off versus N expensive
parallel guesses we simply can't afford to run; we did not benchmark best-of-N.

### Storing the solution code in the external memory service
**Rejected for fidelity.** A memory/RAG service may summarize, chunk, or truncate stored text;
for *code*, any mangling is a correctness bug. We keep bodies **verbatim locally** and let the
service index only the instruction (see chosen technique #3).

---

## Anti-overfit methodology

The benchmark ships gold solutions only for `train` and `dev`; `test_*` ship none. That makes
**demo leakage** the central evaluation hazard.

### The concrete leakage example
Dev tasks come in **sibling variants**. Example family `50e1ac9_1 / _2 / _3`: *"top 4 R&B
songs" / "top 6 EDM songs" / "top 3 indie songs"* — **near-identical instructions** with
**near-identical solution code**. If you seed **dev** gold into the demo store *while
evaluating dev*, a task retrieves its sibling's gold solution — which is essentially the
answer. That's **open-book**: it inflates dev TGC (toward ~100) and **does not generalize** to
unseen test instructions, which have no such sibling in the store.

### The fixes
- **`SEED_SPLITS=train` for an honest dev estimate.** Dev is then *unseen* during dev
  evaluation, mirroring the real test condition. This is the number we trust for iteration.
- **`SEED_SPLITS=train,dev` only for the real test run.** No leakage there: test instructions
  are *not* in the gold seed, so seeding dev simply adds more analogous (not identical)
  examples.
- **Deterministic held-out slice** (`arena/splits.py`) — a stable, hash-chosen subset we
  **never** tune against. Our overfit early-warning.
- **The intended rule:** every "smart" feature must improve **held-out** TGC or be reverted.
  No per-task special-casing in code or prompt, ever. Knowledge is *retrieved/discovered*,
  not memorized.

> **Honesty note on how far this was applied.** The protocol and tooling are in place, but
> only the **prompt-discipline change** was actually measured this way (dev 79.0 → 100.0,
> reported with its leakage caveat). The **verifier** and **rolling-summary compaction** are
> justified against *observed* failure modes (e.g. the empty-answer submission we saw in a
> smoke test) — their clean per-feature held-out A/B on the **graded** model is **pending**:
> the mandated Groq free tier (100K tokens/day) exhausted before the comparison could run. We
> state this rather than imply measured gains we don't have.

---

## Interpreting the results

> **The numbers below are reference measurements on GPT-5.5, which was *not* the final graded
> model** (the graded model became Gemini). Absolute TGC is model-dependent; the harness is
> the contribution.

- **Prompt-discipline fix: dev 79.0 → ~100.** A large jump — but **leakage-inflated** (dev
  gold seeded while evaluating dev; sibling variants make it open-book) **and** on a
  non-graded model. We report it transparently as *not* a generalization signal.
- **Leak-free `test_normal`: preliminary (partial run).** `SEED_SPLITS=train,dev`; test
  instructions unseen; GPT-5.5 (not the graded model). At the time of writing a run was *in
  progress* as proof, tracking ~85–90% TGC over the first ~100/168 tasks — **this is not a
  final figure**; the official number is pending run completion. For calibration, a strong
  scaffold on a strong base model is expected to land between the best scaffold-only
  leaderboard entry (**68.5**) and the RL-trained SOTA (**86.9**).

**Calibration table (leaderboard, GPT-4o unless noted):**

| Approach | TGC |
|---|---|
| Plain ReAct | 48.8 |
| PlanExec (explicit planning) | 44.6 |
| **ReAct + retrieved demos** (best scaffold-only) | **68.5** |
| RL-trained SOTA (requires training) | 86.9 |

**Bottom line.** The contribution is a model-agnostic, test-driven harness with a
leaderboard-proven retrieval lever, a verifier matched to the strict evaluator, fair
pluggable memory, and an evaluation protocol that refuses to fool itself. The score follows
the model; the engineering
is what transfers.
</content>
