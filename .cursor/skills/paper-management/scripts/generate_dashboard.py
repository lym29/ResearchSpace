#!/usr/bin/env python3
"""
Generate HTML dashboard for paper reading progress.
Reads from papers/*.json and notes/ folder to create a visual progress tracker.
"""

import json
import os
from datetime import datetime
from pathlib import Path


def load_json(filepath):
    """Load JSON file, return empty list/dict if file doesn't exist or is empty."""
    try:
        with open(filepath, 'r') as f:
            content = f.read().strip()
            if not content:
                return [] if 'to_read' in filepath or 'read' in filepath else {}
            return json.loads(content)
    except FileNotFoundError:
        return [] if 'to_read' in filepath or 'read' in filepath else {}


def get_note_files(paper_title):
    """Get note files for a paper (markdown files matching the paper title)."""
    notes_dir = Path('paper_management/notes')
    if not notes_dir.exists():
        return []
    
    # Look for markdown files that might be related to this paper
    safe_title = paper_title.replace(':', '').replace('/', '-')
    pattern_variants = [
        f"{safe_title}.md",
        f"{safe_title.lower()}.md",
        f"{safe_title.replace(' ', '_')}.md",
        f"{safe_title.replace(' ', '-')}.md",
    ]
    
    note_files = []
    for note_file in notes_dir.glob('*.md'):
        if note_file.name in pattern_variants:
            note_files.append(note_file.name)
    
    return note_files


def calculate_progress(paper_title, paper_todos):
    """Calculate reading progress for a paper based on TODOs."""
    if paper_title not in paper_todos:
        return 0, 0, 0
    
    todos = paper_todos[paper_title].get('todos', [])
    if not todos:
        return 0, 0, 0
    
    total = len(todos)
    completed = sum(1 for todo in todos if todo.get('completed', False))
    percentage = int((completed / total) * 100) if total > 0 else 0
    
    return completed, total, percentage


def generate_html():
    """Generate the HTML dashboard."""
    
    # Load data
    to_read = load_json('paper_management/papers/to_read.json')
    read = load_json('paper_management/papers/read.json')
    paper_todos = load_json('paper_management/papers/paper_todos.json')
    
    # Calculate statistics
    total_papers = len(to_read) + len(read)
    papers_read = len(read)
    papers_to_read = len(to_read)
    
    # Calculate total todos
    total_todos = 0
    completed_todos = 0
    for paper_data in paper_todos.values():
        todos = paper_data.get('todos', [])
        total_todos += len(todos)
        completed_todos += sum(1 for todo in todos if todo.get('completed', False))
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Paper Reading Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
        }}
        
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-number {{
            font-size: 3em;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .stat-label {{
            font-size: 1em;
            color: #666;
            margin-top: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 50px;
        }}
        
        .section-title {{
            font-size: 1.8em;
            margin-bottom: 20px;
            color: #667eea;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .section-title::before {{
            content: '';
            display: block;
            width: 5px;
            height: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 3px;
        }}
        
        .paper-card {{
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            transition: all 0.3s;
        }}
        
        .paper-card:hover {{
            border-color: #667eea;
            box-shadow: 0 8px 16px rgba(102, 126, 234, 0.2);
        }}
        
        .paper-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 15px;
            gap: 20px;
        }}
        
        .paper-title {{
            font-size: 1.4em;
            font-weight: 600;
            color: #2d3748;
            flex: 1;
        }}
        
        .paper-title a {{
            color: #667eea;
            text-decoration: none;
            transition: color 0.2s;
        }}
        
        .paper-title a:hover {{
            color: #764ba2;
            text-decoration: underline;
        }}
        
        .priority-badge {{
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .priority-high {{
            background: #fee;
            color: #c53030;
        }}
        
        .priority-medium {{
            background: #fef5e7;
            color: #d97706;
        }}
        
        .priority-low {{
            background: #e6f7ff;
            color: #1890ff;
        }}
        
        .paper-authors {{
            color: #718096;
            font-size: 0.95em;
            margin-bottom: 12px;
        }}
        
        .paper-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            font-size: 0.9em;
            color: #718096;
            margin-bottom: 12px;
        }}
        
        .paper-meta span {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        
        .tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 15px;
        }}
        
        .tag {{
            background: #e9ecef;
            color: #495057;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
        }}
        
        .progress-section {{
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #e9ecef;
        }}
        
        .progress-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        
        .progress-label {{
            font-weight: 600;
            color: #4a5568;
        }}
        
        .progress-percent {{
            font-weight: 700;
            color: #667eea;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 10px;
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 15px;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s;
        }}
        
        .todos {{
            margin-top: 15px;
        }}
        
        .todo-item {{
            display: flex;
            align-items: start;
            gap: 10px;
            padding: 8px 0;
            color: #4a5568;
        }}
        
        .todo-checkbox {{
            width: 20px;
            height: 20px;
            border: 2px solid #cbd5e0;
            border-radius: 4px;
            flex-shrink: 0;
            margin-top: 2px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .todo-checkbox.completed {{
            background: #667eea;
            border-color: #667eea;
        }}
        
        .todo-checkbox.completed::after {{
            content: '✓';
            color: white;
            font-weight: bold;
        }}
        
        .todo-text {{
            flex: 1;
        }}
        
        .todo-text.completed {{
            text-decoration: line-through;
            opacity: 0.6;
        }}
        
        .notes-link {{
            display: inline-flex;
            align-items: center;
            gap: 5px;
            color: #667eea;
            text-decoration: none;
            font-size: 0.9em;
            margin-top: 10px;
            padding: 5px 10px;
            background: #f0f4ff;
            border-radius: 6px;
            transition: background 0.2s;
        }}
        
        .notes-link:hover {{
            background: #e0e7ff;
        }}
        
        .empty-state {{
            text-align: center;
            padding: 60px 20px;
            color: #718096;
        }}
        
        .empty-state-icon {{
            font-size: 4em;
            margin-bottom: 20px;
            opacity: 0.5;
        }}
        
        .footer {{
            text-align: center;
            padding: 30px;
            background: #f8f9fa;
            color: #718096;
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            .paper-header {{
                flex-direction: column;
            }}
            
            .stats {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Research Paper Reading Dashboard</h1>
            <p>Track your reading progress and manage your research papers</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{total_papers}</div>
                <div class="stat-label">Total Papers</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{papers_read}</div>
                <div class="stat-label">Papers Read</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{papers_to_read}</div>
                <div class="stat-label">To Read</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{completed_todos}/{total_todos}</div>
                <div class="stat-label">TODOs Completed</div>
            </div>
        </div>
        
        <div class="content">
"""
    
    # Add "To Read" section
    html += """
            <div class="section">
                <h2 class="section-title">📖 Currently Reading / To Read</h2>
"""
    
    if to_read:
        for paper in to_read:
            title = paper.get('title', 'Untitled')
            authors = paper.get('authors', 'Unknown authors')
            url = paper.get('url', '#')
            added_date = paper.get('added_date', 'N/A')
            priority = paper.get('priority', 'medium')
            tags = paper.get('tags', [])
            notes_preview = paper.get('notes', '')
            
            # Truncate notes preview
            if notes_preview and len(notes_preview) > 200:
                notes_preview = notes_preview[:200] + '...'
            
            # Get progress
            completed, total, percentage = calculate_progress(title, paper_todos)
            
            # Get note files
            note_files = get_note_files(title)
            
            html += f"""
                <div class="paper-card">
                    <div class="paper-header">
                        <div class="paper-title">
                            <a href="{url}" target="_blank">{title}</a>
                        </div>
                        <span class="priority-badge priority-{priority}">{priority}</span>
                    </div>
                    <div class="paper-authors">{authors}</div>
                    <div class="paper-meta">
                        <span>📅 Added: {added_date}</span>
"""
            
            if note_files:
                html += f"""
                        <span>📝 Notes: {len(note_files)} file(s)</span>
"""
            
            html += """
                    </div>
"""
            
            if tags:
                html += """
                    <div class="tags">
"""
                for tag in tags:
                    html += f"""
                        <span class="tag">{tag}</span>
"""
                html += """
                    </div>
"""
            
            if notes_preview:
                html += f"""
                    <p style="color: #4a5568; font-size: 0.95em; line-height: 1.6; margin-top: 10px;">{notes_preview}</p>
"""
            
            # Progress section
            if title in paper_todos:
                todos = paper_todos[title].get('todos', [])
                
                html += f"""
                    <div class="progress-section">
                        <div class="progress-header">
                            <span class="progress-label">Reading Progress</span>
                            <span class="progress-percent">{percentage}%</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {percentage}%"></div>
                        </div>
"""
                
                if todos:
                    html += """
                        <div class="todos">
"""
                    for todo in todos:
                        task = todo.get('task', '')
                        completed = todo.get('completed', False)
                        completed_class = 'completed' if completed else ''
                        
                        html += f"""
                            <div class="todo-item">
                                <div class="todo-checkbox {completed_class}"></div>
                                <div class="todo-text {completed_class}">{task}</div>
                            </div>
"""
                    html += """
                        </div>
"""
                
                html += """
                    </div>
"""
            
            # Note files links
            if note_files:
                for note_file in note_files:
                    html += f"""
                    <a href="paper_management/notes/{note_file}" class="notes-link">
                        📝 View Notes: {note_file}
                    </a>
"""
            
            html += """
                </div>
"""
    else:
        html += """
                <div class="empty-state">
                    <div class="empty-state-icon">📭</div>
                    <p>No papers to read yet. Add some papers to get started!</p>
                </div>
"""
    
    html += """
            </div>
"""
    
    # Add "Completed" section
    html += """
            <div class="section">
                <h2 class="section-title">✅ Completed Papers</h2>
"""
    
    if read:
        for paper in read:
            title = paper.get('title', 'Untitled')
            authors = paper.get('authors', 'Unknown authors')
            url = paper.get('url', '#')
            completed_date = paper.get('completed_date', 'N/A')
            tags = paper.get('tags', [])
            
            # Get note files
            note_files = get_note_files(title)
            
            html += f"""
                <div class="paper-card">
                    <div class="paper-header">
                        <div class="paper-title">
                            <a href="{url}" target="_blank">{title}</a>
                        </div>
                    </div>
                    <div class="paper-authors">{authors}</div>
                    <div class="paper-meta">
                        <span>✓ Completed: {completed_date}</span>
"""
            
            if note_files:
                html += f"""
                        <span>📝 Notes: {len(note_files)} file(s)</span>
"""
            
            html += """
                    </div>
"""
            
            if tags:
                html += """
                    <div class="tags">
"""
                for tag in tags:
                    html += f"""
                        <span class="tag">{tag}</span>
"""
                html += """
                    </div>
"""
            
            # Note files links
            if note_files:
                for note_file in note_files:
                    html += f"""
                    <a href="paper_management/notes/{note_file}" class="notes-link">
                        📝 View Notes: {note_file}
                    </a>
"""
            
            html += """
                </div>
"""
    else:
        html += """
                <div class="empty-state">
                    <div class="empty-state-icon">🎯</div>
                    <p>No completed papers yet. Keep reading!</p>
                </div>
"""
    
    html += """
            </div>
        </div>
        
        <div class="footer">
"""
    
    html += f"""
            Last updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
"""
    
    html += """
        </div>
    </div>
</body>
</html>
"""
    
    return html


def main():
    """Main function to generate and save the dashboard."""
    html = generate_html()
    
    # Save to file
    output_file = 'reading_progress.html'
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"Dashboard generated successfully: {output_file}")
    print("Open the file in your browser to view your reading progress!")


if __name__ == '__main__':
    main()
