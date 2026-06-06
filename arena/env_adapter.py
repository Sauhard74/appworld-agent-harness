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
