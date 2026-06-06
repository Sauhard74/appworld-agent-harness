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
