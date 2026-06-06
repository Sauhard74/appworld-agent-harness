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
