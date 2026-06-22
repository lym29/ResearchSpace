#!/usr/bin/env python3
"""Local web server for an interactive reading dashboard."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from dashboard_data import load_dashboard_data
from paper_todo_skill import PaperTodoManager

INTERACTIVE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Research Paper Reading Dashboard</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh; padding: 20px; color: #333;
    }
    .container {
      max-width: 1400px; margin: 0 auto; background: white;
      border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); overflow: hidden;
    }
    .header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white; padding: 32px 40px; text-align: center;
    }
    .header h1 { font-size: 2.2em; margin-bottom: 8px; }
    .header p { opacity: 0.9; }
    .banner {
      background: #eef2ff; color: #4338ca; padding: 12px 20px;
      text-align: center; font-size: 0.95em; border-bottom: 1px solid #c7d2fe;
    }
    .stats {
      display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 16px; padding: 28px 40px; background: #f8f9fa;
    }
    .stat-card {
      background: white; padding: 20px; border-radius: 14px; text-align: center;
      box-shadow: 0 4px 6px rgba(0,0,0,0.08);
    }
    .stat-number { font-size: 2.4em; font-weight: 700; color: #667eea; }
    .stat-label {
      margin-top: 8px; color: #666; text-transform: uppercase;
      letter-spacing: 0.08em; font-size: 0.8em;
    }
    .content { padding: 32px 40px 40px; }
    .section { margin-bottom: 40px; }
    .section-title {
      font-size: 1.5em; margin-bottom: 16px; color: #667eea;
      display: flex; align-items: center; gap: 10px;
    }
    .paper-card {
      border: 2px solid #e9ecef; border-radius: 14px; padding: 22px;
      margin-bottom: 16px; background: white;
    }
    .paper-header {
      display: flex; justify-content: space-between; gap: 16px;
      align-items: start; margin-bottom: 10px;
    }
    .paper-title { font-size: 1.25em; font-weight: 600; flex: 1; }
    .paper-title a { color: #667eea; text-decoration: none; }
    .paper-title a:hover { text-decoration: underline; }
    .paper-authors { color: #718096; margin-bottom: 10px; font-size: 0.95em; }
    .priority-badge {
      padding: 4px 12px; border-radius: 999px; font-size: 0.75em;
      font-weight: 700; text-transform: uppercase;
    }
    .priority-high { background: #fee; color: #c53030; }
    .priority-medium { background: #fef5e7; color: #d97706; }
    .priority-low { background: #e6f7ff; color: #1890ff; }
    .tags { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; }
    .tag { background: #e9ecef; padding: 4px 10px; border-radius: 999px; font-size: 0.82em; }
    .progress-section {
      margin-top: 16px; padding-top: 16px; border-top: 1px solid #e9ecef;
    }
    .progress-header {
      display: flex; justify-content: space-between; margin-bottom: 8px; font-weight: 600;
    }
    .progress-bar {
      height: 10px; background: #e9ecef; border-radius: 999px; overflow: hidden; margin-bottom: 12px;
    }
    .progress-fill {
      height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); transition: width 0.25s ease;
    }
    .todo-item { display: flex; align-items: center; gap: 10px; padding: 8px 0; }
    .todo-item input[type="checkbox"] {
      width: 18px; height: 18px; accent-color: #667eea; cursor: pointer;
    }
    .todo-text {
      flex: 1; border: 1px solid transparent; border-radius: 6px;
      padding: 6px 8px; font: inherit; color: #4a5568; background: transparent;
    }
    .todo-text:focus { outline: none; border-color: #667eea; background: #f8faff; }
    .todo-text.completed { text-decoration: line-through; opacity: 0.6; }
    .todo-delete {
      border: none; background: transparent; color: #a0aec0;
      cursor: pointer; font-size: 1.1em; padding: 4px 8px;
    }
    .todo-delete:hover { color: #e53e3e; }
    .add-todo { display: flex; gap: 8px; margin-top: 10px; }
    .add-todo input {
      flex: 1; border: 1px solid #cbd5e0; border-radius: 8px; padding: 8px 10px; font: inherit;
    }
    .add-todo button, .refresh-btn {
      border: none; border-radius: 8px; padding: 8px 14px;
      background: #667eea; color: white; cursor: pointer; font: inherit;
    }
    .add-todo button:hover, .refresh-btn:hover { background: #5a67d8; }
    .toolbar {
      display: flex; justify-content: space-between; align-items: center;
      margin-bottom: 16px; color: #718096; font-size: 0.9em;
    }
    .empty-state { text-align: center; padding: 40px 20px; color: #718096; }
    .footer {
      text-align: center; padding: 24px; background: #f8f9fa; color: #718096; font-size: 0.9em;
    }
    .toast {
      position: fixed; bottom: 24px; right: 24px; background: #1a202c; color: white;
      padding: 12px 16px; border-radius: 10px; opacity: 0; transform: translateY(10px);
      transition: all 0.2s ease; pointer-events: none; z-index: 1000;
    }
    .toast.show { opacity: 1; transform: translateY(0); }
    .toast.error { background: #c53030; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Research Paper Reading Dashboard</h1>
    </div>
    <div class="banner">Changes save automatically to your local <code>papers/paper_todos.json</code> file.</div>
    <div class="stats" id="stats"></div>
    <div class="content">
      <div class="toolbar">
        <span id="updated-at"></span>
        <button class="refresh-btn" onclick="loadDashboard()">Refresh</button>
      </div>
      <div class="section">
        <h2 class="section-title">Currently Reading / To Read</h2>
        <div id="to-read-list"></div>
      </div>
      <div class="section">
        <h2 class="section-title">Completed Papers</h2>
        <div id="read-list"></div>
      </div>
    </div>
    <div class="footer" id="footer"></div>
  </div>
  <div class="toast" id="toast"></div>
  <script>
    function showToast(message, isError = false) {
      const toast = document.getElementById('toast');
      toast.textContent = message;
      toast.className = 'toast show' + (isError ? ' error' : '');
      setTimeout(() => { toast.className = 'toast'; }, 2200);
    }

    async function api(path, method = 'GET', body = null) {
      const options = { method, headers: { 'Content-Type': 'application/json' } };
      if (body) options.body = JSON.stringify(body);
      const response = await fetch(path, options);
      const data = await response.json();
      if (!response.ok || data.success === false) {
        throw new Error(data.message || 'Request failed');
      }
      return data;
    }

    function escapeHtml(text) {
      const div = document.createElement('div');
      div.textContent = text || '';
      return div.innerHTML;
    }

    function renderStats(stats) {
      document.getElementById('stats').innerHTML = `
        <div class="stat-card"><div class="stat-number">${stats.total_papers}</div><div class="stat-label">Total Papers</div></div>
        <div class="stat-card"><div class="stat-number">${stats.papers_read}</div><div class="stat-label">Papers Read</div></div>
        <div class="stat-card"><div class="stat-number">${stats.papers_to_read}</div><div class="stat-label">To Read</div></div>
        <div class="stat-card"><div class="stat-number">${stats.completed_todos}/${stats.total_todos}</div><div class="stat-label">TODOs Completed</div></div>
      `;
    }

    function renderTodoSection(paperTitle, paperTodos) {
      const entry = paperTodos[paperTitle];
      if (!entry) {
        return `
          <div class="progress-section">
            <p style="color:#718096; margin-bottom:10px;">No reading plan yet.</p>
            <div class="add-todo">
              <input type="text" placeholder="Add first TODO..." data-paper-title="${escapeHtml(paperTitle)}">
              <button onclick="addTodoFromInput(this.previousElementSibling, true)">Add</button>
            </div>
          </div>
        `;
      }

      const todos = entry.todos || [];
      const completed = todos.filter(t => t.completed).length;
      const total = todos.length;
      const percentage = total ? Math.round((completed / total) * 100) : 0;

      const todoItems = todos.map((todo, index) => `
        <div class="todo-item" data-paper-title="${escapeHtml(paperTitle)}" data-index="${index}">
          <input type="checkbox" ${todo.completed ? 'checked' : ''} onchange="toggleTodo(this)">
          <input class="todo-text ${todo.completed ? 'completed' : ''}" value="${escapeHtml(todo.task)}"
            onchange="updateTodo(this)" onkeydown="if (event.key === 'Enter') this.blur()">
          <button class="todo-delete" title="Delete TODO" onclick="deleteTodo(this)">×</button>
        </div>
      `).join('');

      return `
        <div class="progress-section">
          <div class="progress-header"><span>Reading Progress</span><span>${percentage}%</span></div>
          <div class="progress-bar"><div class="progress-fill" style="width:${percentage}%"></div></div>
          <div class="todos">${todoItems}</div>
          <div class="add-todo">
            <input type="text" placeholder="Add a TODO..." data-paper-title="${escapeHtml(paperTitle)}">
            <button onclick="addTodoFromInput(this.previousElementSibling)">Add</button>
          </div>
        </div>
      `;
    }

    function renderPaperCard(paper, paperTodos, showProgress = true) {
      const title = paper.title || 'Untitled';
      const tags = (paper.tags || []).map(tag => `<span class="tag">${escapeHtml(tag)}</span>`).join('');
      const priority = paper.priority || 'medium';
      return `
        <div class="paper-card">
          <div class="paper-header">
            <div class="paper-title"><a href="${escapeHtml(paper.url || '#')}" target="_blank">${escapeHtml(title)}</a></div>
            ${showProgress ? `<span class="priority-badge priority-${priority}">${escapeHtml(priority)}</span>` : ''}
          </div>
          <div class="paper-authors">${escapeHtml(paper.authors || 'Unknown authors')}</div>
          ${tags ? `<div class="tags">${tags}</div>` : ''}
          ${showProgress ? renderTodoSection(title, paperTodos) : ''}
        </div>
      `;
    }

    function renderDashboard(data) {
      renderStats(data.stats);
      document.getElementById('updated-at').textContent =
        'Last updated: ' + new Date(data.updated_at).toLocaleString();
      document.getElementById('footer').textContent =
        'Interactive dashboard running locally. Keep this server open while editing.';

      const toRead = data.to_read || [];
      const read = data.read || [];
      const paperTodos = data.paper_todos || {};

      document.getElementById('to-read-list').innerHTML = toRead.length
        ? toRead.map(paper => renderPaperCard(paper, paperTodos, true)).join('')
        : '<div class="empty-state">No papers to read yet.</div>';

      document.getElementById('read-list').innerHTML = read.length
        ? read.map(paper => renderPaperCard(paper, paperTodos, false)).join('')
        : '<div class="empty-state">No completed papers yet.</div>';
    }

    async function loadDashboard() {
      const response = await fetch('/api/dashboard');
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.message || 'Request failed');
      }
      lastRevision = data.revision;
      renderDashboard(data);
    }

    let lastRevision = null;

    function isEditing() {
      const active = document.activeElement;
      if (!active) return false;
      if (active.classList.contains('todo-text')) return true;
      return Boolean(active.closest('.add-todo'));
    }

    async function pollDashboard() {
      if (isEditing()) return;
      try {
        const response = await fetch('/api/dashboard');
        const data = await response.json();
        if (!response.ok) return;
        if (lastRevision !== null && data.revision === lastRevision) return;
        lastRevision = data.revision;
        renderDashboard(data);
        showToast('Dashboard updated');
      } catch (error) {
        // Server may be restarting; ignore transient poll failures.
      }
    }

    setInterval(pollDashboard, 3000);

    function getTodoContext(element) {
      const item = element.closest('.todo-item');
      return {
        paperTitle: item.dataset.paperTitle,
        index: Number(item.dataset.index),
      };
    }

    async function toggleTodo(checkbox) {
      const { paperTitle, index } = getTodoContext(checkbox);
      try {
        await api('/api/todos/toggle', 'POST', { paper_title: paperTitle, index });
        await loadDashboard();
        showToast('TODO updated');
      } catch (error) {
        showToast(error.message, true);
      }
    }

    async function updateTodo(input) {
      const { paperTitle, index } = getTodoContext(input);
      try {
        await api('/api/todos/update', 'PUT', {
          paper_title: paperTitle,
          index,
          task: input.value,
        });
        showToast('TODO saved');
      } catch (error) {
        showToast(error.message, true);
        await loadDashboard();
      }
    }

    async function deleteTodo(button) {
      const { paperTitle, index } = getTodoContext(button);
      try {
        await api('/api/todos/delete', 'DELETE', { paper_title: paperTitle, index });
        await loadDashboard();
        showToast('TODO deleted');
      } catch (error) {
        showToast(error.message, true);
      }
    }

    async function addTodoFromInput(input, createPlan = false) {
      const paperTitle = input.dataset.paperTitle;
      const task = input.value.trim();
      if (!task) return;
      try {
        await api('/api/todos/add', 'POST', { paper_title: paperTitle, task });
        input.value = '';
        await loadDashboard();
        showToast(createPlan ? 'Reading plan created' : 'TODO added');
      } catch (error) {
        showToast(error.message, true);
      }
    }

    loadDashboard().catch(error => showToast(error.message, true));
  </script>
</body>
</html>
"""


class DashboardHandler(BaseHTTPRequestHandler):
    """HTTP handler for dashboard UI and TODO API."""

    def log_message(self, format, *args):
        return

    def _read_json_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        return json.loads(raw) if raw else {}

    def _send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html):
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            self._send_html(INTERACTIVE_HTML)
            return
        if path == "/api/dashboard":
            self._send_json(load_dashboard_data())
            return
        self._send_json({"success": False, "message": "Not found"}, status=404)

    def do_POST(self):
        path = urlparse(self.path).path
        body = self._read_json_body()
        manager = PaperTodoManager()

        if path == "/api/todos/toggle":
            success, message, paper_key, _task = manager.toggle_todo(
                body.get("paper_title", ""), body.get("index", -1)
            )
            self._send_json(
                {"success": success, "message": message, "paper_title": paper_key},
                status=200 if success else 400,
            )
            return

        if path == "/api/todos/add":
            paper_title = body.get("paper_title", "")
            task = body.get("task", "")
            if not manager.find_paper_key(paper_title):
                manager.create_todo_list(paper_title, todos=[task])
                self._send_json(
                    {"success": True, "message": f"Created reading plan for {paper_title}"}
                )
                return
            success, message, paper_key = manager.add_todo_item(paper_title, task)
            self._send_json(
                {"success": success, "message": message, "paper_title": paper_key},
                status=200 if success else 400,
            )
            return

        self._send_json({"success": False, "message": "Not found"}, status=404)

    def do_PUT(self):
        path = urlparse(self.path).path
        body = self._read_json_body()
        manager = PaperTodoManager()

        if path == "/api/todos/update":
            success, message, paper_key = manager.update_todo_item(
                body.get("paper_title", ""),
                body.get("index", -1),
                body.get("task", ""),
            )
            self._send_json(
                {"success": success, "message": message, "paper_title": paper_key},
                status=200 if success else 400,
            )
            return

        self._send_json({"success": False, "message": "Not found"}, status=404)

    def do_DELETE(self):
        path = urlparse(self.path).path
        body = self._read_json_body()
        manager = PaperTodoManager()

        if path == "/api/todos/delete":
            success, message, paper_key, _deleted = manager.delete_todo_item(
                body.get("paper_title", ""),
                todo_index=body.get("index", -1),
            )
            self._send_json(
                {"success": success, "message": message, "paper_title": paper_key},
                status=200 if success else 400,
            )
            return

        self._send_json({"success": False, "message": "Not found"}, status=404)


def run_server(host="127.0.0.1", port=8765):
    server = ThreadingHTTPServer((host, port), DashboardHandler)
    url = f"http://{host}:{port}/"
    print(f"Interactive dashboard running at {url}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard server stopped.")
        server.server_close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the interactive reading dashboard server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    run_server(host=args.host, port=args.port)
