"""Shared paths for ResearchSpace user data (papers, notes, dashboard)."""

import os
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
_SKILL_MARKER = Path(".cursor") / "skills" / "paper-management"


def get_workspace_root() -> Path:
    """Resolve the workspace root where user data should live."""
    env_root = os.environ.get("RESEARCH_SPACE_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()

    for start in (Path.cwd(), _SCRIPTS_DIR):
        current = start.resolve()
        if current.is_file():
            current = current.parent
        for _ in range(12):
            if (current / _SKILL_MARKER).exists():
                return current
            if (current / "papers").is_dir():
                return current
            parent = current.parent
            if parent == current:
                break
            current = parent

    return Path.cwd().resolve()


WORKSPACE_ROOT = get_workspace_root()
PAPERS_DIR = WORKSPACE_ROOT / "papers"
NOTES_DIR = WORKSPACE_ROOT / "notes"
TO_READ_FILE = PAPERS_DIR / "to_read.json"
READ_FILE = PAPERS_DIR / "read.json"
PAPER_TODOS_FILE = PAPERS_DIR / "paper_todos.json"
DASHBOARD_FILE = WORKSPACE_ROOT / "reading_progress.html"
SCRIPTS_DIR = _SCRIPTS_DIR
