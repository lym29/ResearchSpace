#!/usr/bin/env python3
"""
Paper TODO List Skill - Agent-friendly interface for managing paper reading TODOs

This module provides a system for creating and managing TODO lists for papers,
helping you organize tasks related to reading, understanding, and working with papers.

Usage:
    from paper_todo_skill import create_paper_todo, add_todo_item, mark_todo_complete
    
    # Create a TODO list for a paper
    result = create_paper_todo(
        "Attention Is All You Need",
        todos=[
            "Read abstract and introduction",
            "Understand the transformer architecture",
            "Study the attention mechanism",
            "Review the experimental results"
        ]
    )
    
    # Add a new TODO item
    result = add_todo_item(
        "Attention Is All You Need",
        "Implement a simple transformer in PyTorch"
    )
    
    # Mark a TODO as complete
    result = mark_todo_complete(
        "Attention Is All You Need",
        "Read abstract and introduction"
    )
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

BASE_DIR = Path(__file__).parent
PAPER_TODOS_FILE = BASE_DIR / "papers" / "paper_todos.json"


class PaperTodoManager:
    """Manages TODO lists for papers"""
    
    def __init__(self):
        self.todos = self._load_todos()
    
    def _load_todos(self) -> Dict:
        """Load paper TODOs from JSON file"""
        if not PAPER_TODOS_FILE.exists():
            return {}
        try:
            with open(PAPER_TODOS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    
    def _save_todos(self):
        """Save paper TODOs to JSON file"""
        PAPER_TODOS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(PAPER_TODOS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.todos, f, indent=2, ensure_ascii=False)
    
    def find_paper_key(self, paper_title: str) -> Optional[str]:
        """Find paper key by title (case-insensitive partial match)"""
        title_lower = paper_title.lower()
        for key in self.todos.keys():
            if title_lower in key.lower() or key.lower() in title_lower:
                return key
        return None
    
    def create_todo_list(self, paper_title: str, todos: List[str] = None, 
                        priority: str = "medium", notes: str = None) -> bool:
        """Create a new TODO list for a paper"""
        existing_key = self.find_paper_key(paper_title)
        if existing_key:
            return False
        
        todo_items = []
        if todos:
            for todo_text in todos:
                todo_items.append({
                    "task": todo_text,
                    "completed": False,
                    "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
        
        self.todos[paper_title] = {
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "priority": priority,
            "notes": notes or "",
            "todos": todo_items
        }
        self._save_todos()
        return True
    
    def add_todo_item(self, paper_title: str, todo_text: str) -> tuple:
        """Add a TODO item to a paper's list
        Returns: (success, message, paper_key)
        """
        paper_key = self.find_paper_key(paper_title)
        
        if not paper_key:
            return (False, f"No TODO list found for paper: {paper_title}", None)
        
        for todo in self.todos[paper_key]["todos"]:
            if todo["task"].lower() == todo_text.lower():
                return (False, f"TODO item already exists: {todo_text}", paper_key)
        
        self.todos[paper_key]["todos"].append({
            "task": todo_text,
            "completed": False,
            "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self._save_todos()
        return (True, f"Added TODO item: {todo_text}", paper_key)
    
    def mark_complete(self, paper_title: str, todo_text: str = None, 
                     todo_index: int = None) -> tuple:
        """Mark a TODO item as complete
        Can specify either todo_text or todo_index
        Returns: (success, message, paper_key, completed_task)
        """
        paper_key = self.find_paper_key(paper_title)
        
        if not paper_key:
            return (False, f"No TODO list found for paper: {paper_title}", None, None)
        
        todos = self.todos[paper_key]["todos"]
        
        if todo_index is not None:
            if 0 <= todo_index < len(todos):
                todos[todo_index]["completed"] = True
                todos[todo_index]["completed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._save_todos()
                return (True, f"Marked as complete: {todos[todo_index]['task']}", 
                       paper_key, todos[todo_index]['task'])
            else:
                return (False, f"Invalid TODO index: {todo_index}", paper_key, None)
        
        if todo_text:
            todo_lower = todo_text.lower()
            for todo in todos:
                if todo_lower in todo["task"].lower():
                    if todo["completed"]:
                        return (False, f"TODO already completed: {todo['task']}", paper_key, None)
                    todo["completed"] = True
                    todo["completed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self._save_todos()
                    return (True, f"Marked as complete: {todo['task']}", paper_key, todo['task'])
            
            return (False, f"TODO item not found: {todo_text}", paper_key, None)
        
        return (False, "Must specify either todo_text or todo_index", paper_key, None)
    
    def mark_incomplete(self, paper_title: str, todo_text: str = None, 
                       todo_index: int = None) -> tuple:
        """Mark a TODO item as incomplete
        Returns: (success, message, paper_key)
        """
        paper_key = self.find_paper_key(paper_title)
        
        if not paper_key:
            return (False, f"No TODO list found for paper: {paper_title}", None)
        
        todos = self.todos[paper_key]["todos"]
        
        if todo_index is not None:
            if 0 <= todo_index < len(todos):
                todos[todo_index]["completed"] = False
                if "completed_date" in todos[todo_index]:
                    del todos[todo_index]["completed_date"]
                self._save_todos()
                return (True, f"Marked as incomplete: {todos[todo_index]['task']}", paper_key)
            else:
                return (False, f"Invalid TODO index: {todo_index}", paper_key)
        
        if todo_text:
            todo_lower = todo_text.lower()
            for todo in todos:
                if todo_lower in todo["task"].lower():
                    todo["completed"] = False
                    if "completed_date" in todo:
                        del todo["completed_date"]
                    self._save_todos()
                    return (True, f"Marked as incomplete: {todo['task']}", paper_key)
            
            return (False, f"TODO item not found: {todo_text}", paper_key)
        
        return (False, "Must specify either todo_text or todo_index", paper_key)
    
    def get_todos(self, paper_title: str = None) -> Dict:
        """Get TODO list(s)
        If paper_title is None, returns all TODO lists
        Otherwise returns specific paper's TODO list
        """
        if paper_title is None:
            return self.todos
        
        paper_key = self.find_paper_key(paper_title)
        if not paper_key:
            return None
        
        return {paper_key: self.todos[paper_key]}
    
    def delete_todo_list(self, paper_title: str) -> tuple:
        """Delete a paper's TODO list
        Returns: (success, message, paper_key)
        """
        paper_key = self.find_paper_key(paper_title)
        
        if not paper_key:
            return (False, f"No TODO list found for paper: {paper_title}", None)
        
        del self.todos[paper_key]
        self._save_todos()
        return (True, f"Deleted TODO list for: {paper_key}", paper_key)
    
    def delete_todo_item(self, paper_title: str, todo_text: str = None,
                        todo_index: int = None) -> tuple:
        """Delete a specific TODO item
        Returns: (success, message, paper_key, deleted_task)
        """
        paper_key = self.find_paper_key(paper_title)
        
        if not paper_key:
            return (False, f"No TODO list found for paper: {paper_title}", None, None)
        
        todos = self.todos[paper_key]["todos"]
        
        if todo_index is not None:
            if 0 <= todo_index < len(todos):
                deleted_task = todos.pop(todo_index)
                self._save_todos()
                return (True, f"Deleted TODO: {deleted_task['task']}", 
                       paper_key, deleted_task['task'])
            else:
                return (False, f"Invalid TODO index: {todo_index}", paper_key, None)
        
        if todo_text:
            todo_lower = todo_text.lower()
            for i, todo in enumerate(todos):
                if todo_lower in todo["task"].lower():
                    deleted_task = todos.pop(i)
                    self._save_todos()
                    return (True, f"Deleted TODO: {deleted_task['task']}", 
                           paper_key, deleted_task['task'])
            
            return (False, f"TODO item not found: {todo_text}", paper_key, None)
        
        return (False, "Must specify either todo_text or todo_index", paper_key, None)
    
    def get_stats(self, paper_title: str = None) -> Dict:
        """Get statistics about TODO lists"""
        if paper_title:
            paper_key = self.find_paper_key(paper_title)
            if not paper_key:
                return None
            
            todos = self.todos[paper_key]["todos"]
            total = len(todos)
            completed = sum(1 for t in todos if t["completed"])
            
            return {
                "paper": paper_key,
                "total": total,
                "completed": completed,
                "remaining": total - completed,
                "progress": (completed / total * 100) if total > 0 else 0
            }
        
        all_stats = []
        for paper_key, data in self.todos.items():
            todos = data["todos"]
            total = len(todos)
            completed = sum(1 for t in todos if t["completed"])
            
            all_stats.append({
                "paper": paper_key,
                "total": total,
                "completed": completed,
                "remaining": total - completed,
                "progress": (completed / total * 100) if total > 0 else 0,
                "priority": data.get("priority", "medium")
            })
        
        return all_stats


def create_paper_todo(paper_title: str, todos: List[str] = None, 
                     priority: str = "medium", notes: str = None) -> Dict:
    """
    Create a TODO list for a paper
    
    Args:
        paper_title: Title of the paper
        todos: List of TODO items as strings
        priority: Priority level ('low', 'medium', 'high')
        notes: Additional notes about the paper or reading plan
    
    Returns:
        Dict with success status and message
    """
    manager = PaperTodoManager()
    
    success = manager.create_todo_list(paper_title, todos, priority, notes)
    
    if success:
        todo_count = len(todos) if todos else 0
        return {
            'success': True,
            'message': f"Created TODO list for '{paper_title}' with {todo_count} items",
            'paper_title': paper_title,
            'todo_count': todo_count
        }
    else:
        return {
            'success': False,
            'message': f"TODO list for '{paper_title}' already exists",
            'paper_title': paper_title
        }


def add_todo_item(paper_title: str, todo_text: str) -> Dict:
    """
    Add a TODO item to a paper's list
    
    Args:
        paper_title: Title of the paper (can be partial)
        todo_text: The TODO item to add
    
    Returns:
        Dict with success status and message
    """
    manager = PaperTodoManager()
    success, message, paper_key = manager.add_todo_item(paper_title, todo_text)
    
    return {
        'success': success,
        'message': message,
        'paper_title': paper_key,
        'todo_item': todo_text if success else None
    }


def mark_todo_complete(paper_title: str, todo_text: str = None, 
                      todo_index: int = None) -> Dict:
    """
    Mark a TODO item as complete
    
    Args:
        paper_title: Title of the paper (can be partial)
        todo_text: The TODO item text (can be partial)
        todo_index: Index of the TODO item (0-based)
    
    Returns:
        Dict with success status and message
    """
    manager = PaperTodoManager()
    success, message, paper_key, completed_task = manager.mark_complete(
        paper_title, todo_text, todo_index
    )
    
    return {
        'success': success,
        'message': message,
        'paper_title': paper_key,
        'completed_task': completed_task
    }


def mark_todo_incomplete(paper_title: str, todo_text: str = None,
                        todo_index: int = None) -> Dict:
    """Mark a TODO item as incomplete"""
    manager = PaperTodoManager()
    success, message, paper_key = manager.mark_incomplete(paper_title, todo_text, todo_index)
    
    return {
        'success': success,
        'message': message,
        'paper_title': paper_key
    }


def get_paper_todos(paper_title: str = None) -> Dict:
    """
    Get TODO list(s) for paper(s)
    
    Args:
        paper_title: Title of the paper (None returns all)
    
    Returns:
        Dict with TODO lists
    """
    manager = PaperTodoManager()
    todos = manager.get_todos(paper_title)
    
    if paper_title and todos is None:
        return {
            'success': False,
            'message': f"No TODO list found for paper: {paper_title}",
            'todos': None
        }
    
    return {
        'success': True,
        'message': 'Retrieved TODO lists',
        'todos': todos
    }


def delete_paper_todos(paper_title: str) -> Dict:
    """Delete a paper's entire TODO list"""
    manager = PaperTodoManager()
    success, message, paper_key = manager.delete_todo_list(paper_title)
    
    return {
        'success': success,
        'message': message,
        'paper_title': paper_key
    }


def delete_todo_item(paper_title: str, todo_text: str = None,
                    todo_index: int = None) -> Dict:
    """Delete a specific TODO item"""
    manager = PaperTodoManager()
    success, message, paper_key, deleted_task = manager.delete_todo_item(
        paper_title, todo_text, todo_index
    )
    
    return {
        'success': success,
        'message': message,
        'paper_title': paper_key,
        'deleted_task': deleted_task
    }


def get_todo_stats(paper_title: str = None) -> Dict:
    """
    Get statistics about TODO lists
    
    Args:
        paper_title: Title of the paper (None returns all)
    
    Returns:
        Dict with statistics
    """
    manager = PaperTodoManager()
    stats = manager.get_stats(paper_title)
    
    if paper_title and stats is None:
        return {
            'success': False,
            'message': f"No TODO list found for paper: {paper_title}",
            'stats': None
        }
    
    return {
        'success': True,
        'message': 'Retrieved statistics',
        'stats': stats
    }


def format_todo_list(paper_title: str = None, show_completed: bool = True) -> str:
    """Format TODO list for display"""
    manager = PaperTodoManager()
    todos = manager.get_todos(paper_title)
    
    if not todos:
        return f"No TODO list found for: {paper_title}" if paper_title else "No TODO lists found"
    
    output = []
    
    for paper_key, data in todos.items():
        output.append("=" * 70)
        output.append(f"📚 {paper_key}")
        output.append("-" * 70)
        
        stats = manager.get_stats(paper_key)
        if stats:
            output.append(f"📊 Progress: {stats['completed']}/{stats['total']} "
                        f"({stats['progress']:.0f}%) | Priority: {data['priority']}")
        
        if data.get('notes'):
            output.append(f"📝 Notes: {data['notes']}")
        
        output.append("")
        output.append("TODO Items:")
        
        todos_list = data["todos"]
        if not todos_list:
            output.append("  (no items)")
        else:
            for i, todo in enumerate(todos_list):
                if not show_completed and todo["completed"]:
                    continue
                
                status = "✅" if todo["completed"] else "⬜"
                output.append(f"  {i}. {status} {todo['task']}")
                
                if todo["completed"] and "completed_date" in todo:
                    output.append(f"      Completed: {todo['completed_date']}")
        
        output.append("")
    
    return "\n".join(output)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Paper TODO List Skill")
        print("\nUsage:")
        print("  Create TODO list:")
        print("    python paper_todo_skill.py create <paper_title>")
        print("  Add TODO item:")
        print("    python paper_todo_skill.py add <paper_title> <todo_text>")
        print("  Mark complete:")
        print("    python paper_todo_skill.py complete <paper_title> <todo_text>")
        print("  View TODOs:")
        print("    python paper_todo_skill.py list [paper_title]")
        print("  View stats:")
        print("    python paper_todo_skill.py stats [paper_title]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'create':
        if len(sys.argv) < 3:
            print("Usage: python paper_todo_skill.py create <paper_title>")
            sys.exit(1)
        
        paper_title = sys.argv[2]
        result = create_paper_todo(paper_title)
        print(result['message'])
        sys.exit(0 if result['success'] else 1)
    
    elif command == 'add':
        if len(sys.argv) < 4:
            print("Usage: python paper_todo_skill.py add <paper_title> <todo_text>")
            sys.exit(1)
        
        paper_title = sys.argv[2]
        todo_text = ' '.join(sys.argv[3:])
        result = add_todo_item(paper_title, todo_text)
        print(result['message'])
        sys.exit(0 if result['success'] else 1)
    
    elif command == 'complete':
        if len(sys.argv) < 4:
            print("Usage: python paper_todo_skill.py complete <paper_title> <todo_text_or_index>")
            sys.exit(1)
        
        paper_title = sys.argv[2]
        todo_ref = ' '.join(sys.argv[3:])
        
        if todo_ref.isdigit():
            result = mark_todo_complete(paper_title, todo_index=int(todo_ref))
        else:
            result = mark_todo_complete(paper_title, todo_text=todo_ref)
        
        print(result['message'])
        sys.exit(0 if result['success'] else 1)
    
    elif command == 'list':
        paper_title = sys.argv[2] if len(sys.argv) > 2 else None
        print(format_todo_list(paper_title))
        sys.exit(0)
    
    elif command == 'stats':
        paper_title = sys.argv[2] if len(sys.argv) > 2 else None
        result = get_todo_stats(paper_title)
        
        if result['success']:
            stats = result['stats']
            if isinstance(stats, list):
                for stat in stats:
                    print(f"{stat['paper']}: {stat['completed']}/{stat['total']} "
                          f"({stat['progress']:.0f}%) - Priority: {stat['priority']}")
            else:
                print(f"{stats['paper']}: {stats['completed']}/{stats['total']} "
                      f"({stats['progress']:.0f}%)")
        else:
            print(result['message'])
        
        sys.exit(0 if result['success'] else 1)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
