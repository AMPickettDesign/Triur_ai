"""
Shared utilities for the sibling AI system.
Common file I/O, JSON helpers, and path constants.
"""

import json
import os

# ─── Paths ───
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_DIR = os.path.join(ROOT_DIR, "config")
DATA_DIR = os.path.join(ROOT_DIR, "data")

# ─── Per-sibling naming conventions ───
# Each sibling gets unique file naming to feel like a different person
SIBLING_NAMING = {
    "abi":   {"prefix": "A",  "reflection": "Diary"},
    "david": {"prefix": "D",  "reflection": "Notebook"},
    "quinn": {"prefix": "Q",  "reflection": "Journal"},
}

def get_sibling_naming(sibling_id):
    """Get the naming convention for a sibling. Falls back to defaults."""
    return SIBLING_NAMING.get(sibling_id, {"prefix": sibling_id[0].upper(), "reflection": "Entry"})

def get_sibling_dirs(sibling_id):
    """Get data directories for a specific sibling."""
    base = os.path.join(DATA_DIR, sibling_id)
    dirs = {
        "memory": os.path.join(base, "memory"),
        "conversations": os.path.join(base, "conversations"),
        "journal": os.path.join(base, "journal"),
    }
    for d in dirs.values():
        os.makedirs(d, exist_ok=True)
    return dirs

def load_json(filepath, default=None):
    """Load a JSON file, return default if missing or invalid."""
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return default if default is not None else {}

def save_json(filepath, data):
    """Save data to a JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def clean_llm_json(text):
    """Strip markdown wrappers from LLM JSON responses and parse."""
    if not text:
        return None
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1].rsplit("```", 1)[0]
    try:
        return json.loads(cleaned)
    except (json.JSONDecodeError, ValueError):
        return None
