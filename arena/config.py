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

# --- Tex memory backend ---
TEX_API_KEY     = os.environ.get("TEX_API_KEY")
TEX_BASE_URL    = os.environ.get("TEX_BASE_URL")
TEX_ORG_ID      = os.environ.get("TEX_ORG_ID")
TEX_USER_ID     = os.environ.get("TEX_USER_ID")
TEX_SESSION_ID  = os.environ.get("TEX_SESSION_ID", "appworld-demos")

# --- Observation handling ---
OBS_HEAD = int(os.environ.get("OBS_HEAD", "2500"))
OBS_TAIL = int(os.environ.get("OBS_TAIL", "1500"))
