#!/usr/bin/env bash
set -euo pipefail
: "${APPWORLD_EXPERIMENT:?set APPWORLD_EXPERIMENT}"
SPLIT="${1:-dev}"
python agent.py
appworld evaluate "$APPWORLD_EXPERIMENT" "$SPLIT"
