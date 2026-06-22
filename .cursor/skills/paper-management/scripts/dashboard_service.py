"""Start and manage the interactive dashboard server."""

import json
import socket
import subprocess
import sys
import time
from pathlib import Path

from paths import SCRIPTS_DIR, WORKSPACE_ROOT

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
SERVER_STATE_FILE = WORKSPACE_ROOT / "papers" / ".dashboard_server.json"


def dashboard_url(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> str:
    return f"http://{host}:{port}/"


def is_port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.3)
        return sock.connect_ex((host, port)) == 0


def is_process_running(pid: int) -> bool:
    try:
        import os

        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _load_state() -> dict:
    if not SERVER_STATE_FILE.exists():
        return {}
    try:
        with open(SERVER_STATE_FILE, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_state(state: dict):
    SERVER_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SERVER_STATE_FILE, "w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)


def _clear_stale_state(host: str, port: int):
    if is_port_open(host, port):
        return

    state = _load_state()
    pid = state.get("pid")
    if pid and not is_process_running(pid):
        SERVER_STATE_FILE.unlink(missing_ok=True)


def regenerate_static_dashboard():
    """Regenerate the read-only HTML snapshot."""
    script = SCRIPTS_DIR / "generate_dashboard.py"
    if not script.exists():
        return

    subprocess.run(
        [sys.executable, str(script)],
        cwd=str(WORKSPACE_ROOT),
        capture_output=True,
        timeout=10,
    )


def ensure_dashboard_server(
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    wait_seconds: float = 2.0,
) -> str:
    """Start the dashboard server in the background if it is not already running."""
    _clear_stale_state(host, port)

    if is_port_open(host, port):
        return dashboard_url(host, port)

    state = _load_state()
    pid = state.get("pid")
    if pid and is_process_running(pid):
        return state.get("url", dashboard_url(host, port))

    server_script = SCRIPTS_DIR / "dashboard_server.py"
    proc = subprocess.Popen(
        [
            sys.executable,
            str(server_script),
            "--host",
            host,
            "--port",
            str(port),
        ],
        cwd=str(WORKSPACE_ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )

    url = dashboard_url(host, port)
    _save_state({"pid": proc.pid, "host": host, "port": port, "url": url})

    deadline = time.time() + wait_seconds
    while time.time() < deadline:
        if is_port_open(host, port):
            return url
        time.sleep(0.1)

    return url


def sync_dashboard(start_server: bool = True) -> str | None:
    """Refresh static dashboard and optionally ensure the live server is running."""
    regenerate_static_dashboard()
    if start_server:
        return ensure_dashboard_server()
    return None


def get_dashboard_url(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> str:
    """Return the dashboard URL, starting the server if needed."""
    return ensure_dashboard_server(host=host, port=port)
