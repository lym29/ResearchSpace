"""Shared helpers for loading dashboard data."""

import json
from datetime import datetime
from pathlib import Path

from paths import TO_READ_FILE, READ_FILE, PAPER_TODOS_FILE


def load_json_file(filepath: Path):
    """Load JSON file, return empty list/dict if missing or empty."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return [] if filepath.name in {"to_read.json", "read.json"} else {}
            return json.loads(content)
    except FileNotFoundError:
        return [] if filepath.name in {"to_read.json", "read.json"} else {}


def calculate_paper_progress(paper_title: str, paper_todos: dict) -> dict:
    """Return completed/total/percentage for a paper's TODO list."""
    if paper_title not in paper_todos:
        return {"completed": 0, "total": 0, "percentage": 0}

    todos = paper_todos[paper_title].get("todos", [])
    total = len(todos)
    completed = sum(1 for todo in todos if todo.get("completed", False))
    percentage = int((completed / total) * 100) if total > 0 else 0
    return {"completed": completed, "total": total, "percentage": percentage}


def get_data_revision() -> str:
    """Stable revision token based on data file modification times."""
    mtimes = []
    for filepath in (TO_READ_FILE, READ_FILE, PAPER_TODOS_FILE):
        if filepath.exists():
            mtimes.append(filepath.stat().st_mtime)
    return str(max(mtimes, default=0.0))


def get_data_updated_at() -> str:
    """Human-readable timestamp for the latest data change."""
    mtimes = [
        filepath.stat().st_mtime
        for filepath in (TO_READ_FILE, READ_FILE, PAPER_TODOS_FILE)
        if filepath.exists()
    ]
    if not mtimes:
        return datetime.now().isoformat()
    return datetime.fromtimestamp(max(mtimes)).isoformat()


def load_dashboard_data() -> dict:
    """Load all dashboard data and summary stats."""
    to_read = load_json_file(TO_READ_FILE)
    read = load_json_file(READ_FILE)
    paper_todos = load_json_file(PAPER_TODOS_FILE)

    total_todos = 0
    completed_todos = 0
    for paper_data in paper_todos.values():
        todos = paper_data.get("todos", [])
        total_todos += len(todos)
        completed_todos += sum(1 for todo in todos if todo.get("completed", False))

    revision = get_data_revision()

    return {
        "to_read": to_read,
        "read": read,
        "paper_todos": paper_todos,
        "stats": {
            "total_papers": len(to_read) + len(read),
            "papers_read": len(read),
            "papers_to_read": len(to_read),
            "completed_todos": completed_todos,
            "total_todos": total_todos,
        },
        "revision": revision,
        "updated_at": get_data_updated_at(),
    }
