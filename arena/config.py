"""Central config. All knobs are env-overridable; defaults are sane for dev iteration."""
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# --- LLM (graded brain) ---
# LLM_API: "chat" = OpenAI-compatible chat/completions (Groq, the MANDATED graded model);
#          "responses" = Azure Responses API (gpt-5.5 etc., for building/experiments only).
LLM_API    = os.environ.get("LLM_API", "chat")
MODEL      = os.environ.get("MODEL", "llama-3.3-70b-versatile")  # graded: Groq Llama 3.3 70B
MAX_OUTPUT_TOKENS = int(os.environ.get("MAX_OUTPUT_TOKENS", "4000"))
TEMPERATURE = float(os.environ.get("TEMPERATURE", "0.0"))

# Groq (chat path)
GROQ_API_KEY  = os.environ.get("GROQ_API_KEY")
GROQ_BASE_URL = os.environ.get("GROQ_BASE_URL", "https://api.groq.com/openai/v1")

# Azure (responses path + ALL embeddings — Groq has no embedding API)
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "text-embedding-3-large")

# --- AppWorld run ---
DATASET    = os.environ.get("APPWORLD_DATASET", "dev")
EXPERIMENT = os.environ.get("APPWORLD_EXPERIMENT", "team_demo")
MAX_TASKS  = int(os.environ.get("MAX_TASKS", "0"))          # 0 = all
MAX_TURNS  = int(os.environ.get("MAX_INTERACTIONS", "40"))
# Cap how much history is RE-SENT each turn (turn-pairs after the initial msg).
# Keeps token cost ~linear on long tasks; full trajectory is still kept internally.
MAX_HISTORY_TURNS = int(os.environ.get("MAX_HISTORY_TURNS", "16"))
VERIFY     = os.environ.get("VERIFY", "1") not in ("0", "false", "False", "")

# --- Retrieval / memory ---
MEMORY_BACKEND = os.environ.get("MEMORY_BACKEND", "local")  # local | tex | hydra
K_DEMOS    = int(os.environ.get("K_DEMOS", "2"))
# Which gold splits seed the demo store. For an HONEST dev number use "train" only
# (dev tasks then unseen, mirroring test). For the real test run, seed "train,dev".
SEED_SPLITS = tuple(s for s in os.environ.get("SEED_SPLITS", "train,dev").split(",") if s)
DATA_DIR   = os.environ.get("DATA_DIR", "data")
CACHE_DIR  = os.environ.get("CACHE_DIR", ".cache")

# --- Tex memory backend ---
TEX_API_KEY     = os.environ.get("TEX_API_KEY")
TEX_BASE_URL    = os.environ.get("TEX_BASE_URL")
TEX_ORG_ID      = os.environ.get("TEX_ORG_ID")
TEX_USER_ID     = os.environ.get("TEX_USER_ID")
TEX_SESSION_ID  = os.environ.get("TEX_SESSION_ID", "appworld-demos")
TEX_SKIP_INGEST = os.environ.get("TEX_SKIP_INGEST", "0") not in ("0", "false", "False", "")

# --- HydraDB memory backend ---
HYDRADB_API_KEY   = os.environ.get("HYDRADB_API_KEY")
HYDRADB_BASE_URL  = os.environ.get("HYDRADB_BASE_URL", "https://api.hydradb.com")
HYDRADB_TENANT_ID = os.environ.get("HYDRADB_TENANT_ID", "appworld-demos")

# --- Observation handling ---
OBS_HEAD = int(os.environ.get("OBS_HEAD", "2500"))
OBS_TAIL = int(os.environ.get("OBS_TAIL", "1500"))
