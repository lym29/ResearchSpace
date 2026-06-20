# Paper TODO List Skill

An agent-friendly system for managing TODO lists for papers, helping you organize reading tasks, understanding goals, and implementation plans.

## Overview

The Paper TODO List Skill allows you to:
- Create TODO lists for papers you're reading
- Track progress through complex papers
- Organize reading goals and implementation tasks
- Mark items as complete/incomplete
- View statistics and progress

## For AI Agents

### Quick Start

```python
from paper_todo_skill import create_paper_todo, add_todo_item, mark_todo_complete

# Create a TODO list for a paper
result = create_paper_todo(
    "Attention Is All You Need",
    todos=[
        "Read abstract and introduction",
        "Understand the transformer architecture",
        "Study the attention mechanism",
        "Review experimental results",
        "Implement a simple transformer"
    ],
    priority="high"
)

# Add a new TODO item
result = add_todo_item(
    "Attention Is All You Need",
    "Compare with LSTM performance"
)

# Mark a TODO as complete
result = mark_todo_complete(
    "Attention Is All You Need",
    "Read abstract and introduction"
)
```

### Agent Usage Patterns

#### Pattern 1: Create TODO list when adding a paper

```python
from paper_skill import add_paper_auto
from paper_todo_skill import create_paper_todo

# User says: "Add this paper and create a reading plan"
paper_result = add_paper_auto("https://arxiv.org/abs/1706.03762")

if paper_result['success']:
    # Create a generic reading plan
    todo_result = create_paper_todo(
        paper_result['paper']['title'],
        todos=[
            "Read abstract and introduction",
            "Understand the main methodology",
            "Review experimental results",
            "Note key contributions",
            "Identify related work"
        ],
        priority=paper_result.get('priority', 'medium')
    )
```

#### Pattern 2: Progressive TODO management

```python
from paper_todo_skill import add_todo_item, mark_todo_complete, get_todo_stats

# User: "I finished reading the intro of the Attention paper"
result = mark_todo_complete(
    "Attention Is All You Need",
    "Read abstract and introduction"
)

# User: "Add a task to implement the positional encoding"
add_todo_item(
    "Attention Is All You Need",
    "Implement positional encoding in code"
)

# Check progress
stats = get_todo_stats("Attention Is All You Need")
print(f"Progress: {stats['stats']['progress']:.0f}%")
```

#### Pattern 3: Custom TODO generation based on paper type

```python
from paper_todo_skill import create_paper_todo

def create_todos_by_type(paper_title, paper_type):
    """Generate appropriate TODOs based on paper type"""
    
    if paper_type == "survey":
        todos = [
            "Read abstract and overview",
            "Identify main categories covered",
            "Note key papers in each category",
            "Understand comparison methodology",
            "Extract future directions"
        ]
    elif paper_type == "implementation":
        todos = [
            "Understand the problem statement",
            "Study the proposed architecture",
            "Review implementation details",
            "Analyze experimental setup",
            "Reproduce key results"
        ]
    elif paper_type == "theory":
        todos = [
            "Understand problem formulation",
            "Follow mathematical derivations",
            "Study proof techniques",
            "Work through examples",
            "Connect to existing theory"
        ]
    else:
        todos = [
            "Read abstract and introduction",
            "Understand methodology",
            "Review results",
            "Note contributions"
        ]
    
    return create_paper_todo(paper_title, todos=todos)

# Usage
create_todos_by_type("Attention Is All You Need", "implementation")
```

#### Pattern 4: Batch operations

```python
from paper_todo_skill import mark_todo_complete, get_paper_todos

# User: "I finished reading the first three sections"
paper_title = "Attention Is All You Need"
todos_result = get_paper_todos(paper_title)

if todos_result['success']:
    todos = todos_result['todos'][paper_title]['todos']
    
    # Mark first 3 as complete
    for i in range(min(3, len(todos))):
        mark_todo_complete(paper_title, todo_index=i)
```

### API Reference

#### `create_paper_todo(paper_title, todos=None, priority="medium", notes=None)`

Create a new TODO list for a paper.

**Parameters:**
- `paper_title` (str, required): Title of the paper
- `todos` (list, optional): List of TODO items as strings
- `priority` (str, optional): Priority level - `"low"`, `"medium"` (default), or `"high"`
- `notes` (str, optional): Notes about reading plan or goals

**Returns:**
```python
{
    'success': bool,
    'message': str,
    'paper_title': str,
    'todo_count': int
}
```

#### `add_todo_item(paper_title, todo_text)`

Add a TODO item to a paper's list.

**Parameters:**
- `paper_title` (str): Title of the paper (can be partial match)
- `todo_text` (str): The TODO item to add

**Returns:**
```python
{
    'success': bool,
    'message': str,
    'paper_title': str,
    'todo_item': str
}
```

#### `mark_todo_complete(paper_title, todo_text=None, todo_index=None)`

Mark a TODO item as complete.

**Parameters:**
- `paper_title` (str): Title of the paper
- `todo_text` (str, optional): TODO item text (can be partial)
- `todo_index` (int, optional): Index of TODO item (0-based)

**Note:** Must specify either `todo_text` or `todo_index`.

**Returns:**
```python
{
    'success': bool,
    'message': str,
    'paper_title': str,
    'completed_task': str
}
```

#### `mark_todo_incomplete(paper_title, todo_text=None, todo_index=None)`

Mark a TODO item as incomplete.

**Parameters:** Same as `mark_todo_complete`

#### `get_paper_todos(paper_title=None)`

Get TODO list(s) for paper(s).

**Parameters:**
- `paper_title` (str, optional): Title of paper (None returns all)

**Returns:**
```python
{
    'success': bool,
    'message': str,
    'todos': dict  # Paper title → TODO data mapping
}
```

#### `delete_paper_todos(paper_title)`

Delete a paper's entire TODO list.

#### `delete_todo_item(paper_title, todo_text=None, todo_index=None)`

Delete a specific TODO item.

#### `get_todo_stats(paper_title=None)`

Get statistics about TODO lists.

**Returns:**
```python
{
    'success': bool,
    'message': str,
    'stats': {
        'paper': str,
        'total': int,
        'completed': int,
        'remaining': int,
        'progress': float  # Percentage
    }
}
```

### Data Structure

TODO lists are stored in `papers/paper_todos.json`:

```json
{
  "Paper Title": {
    "created_date": "2026-06-20 14:30:00",
    "priority": "high",
    "notes": "Focus on understanding the attention mechanism",
    "todos": [
      {
        "task": "Read abstract and introduction",
        "completed": true,
        "added_date": "2026-06-20 14:30:00",
        "completed_date": "2026-06-20 15:45:00"
      },
      {
        "task": "Understand transformer architecture",
        "completed": false,
        "added_date": "2026-06-20 14:30:00"
      }
    ]
  }
}
```

## For Human Users (CLI)

### Basic Usage

```bash
# Create a TODO list
python research.py todos create "Attention Is All You Need" --priority high

# Add TODO items
python research.py todos add "Attention Is All You Need" "Read the introduction"
python research.py todos add "Attention" "Study the attention mechanism"

# List TODOs
python research.py todos list "Attention Is All You Need"
python research.py todos list  # Show all papers

# Mark as complete (by text)
python research.py todos complete "Attention" "Read the introduction"

# Mark as complete (by index)
python research.py todos complete "Attention" 0

# Mark as incomplete
python research.py todos incomplete "Attention" 0

# View statistics
python research.py todos stats "Attention Is All You Need"
python research.py todos stats  # All papers

# Delete a TODO item
python research.py todos delete "Attention" "Read the introduction"
python research.py todos delete "Attention" 0

# Delete entire TODO list
python research.py todos delete "Attention" --all
```

### CLI Options

```bash
todos create <title>
  --priority, -p    Priority: low, medium, high (default: medium)
  --notes, -n       Notes about reading plan

todos add <title> <todo_text>
  # Add a TODO item to the list

todos complete <title> <todo_text_or_index>
  # Mark a TODO as complete

todos incomplete <title> <todo_text_or_index>
  # Mark a TODO as incomplete

todos list [title]
  --show-completed  Show completed items (default)
  --hide-completed  Hide completed items

todos delete <title> [todo_text_or_index]
  --all            Delete entire TODO list

todos stats [title]
  # Show progress statistics
```

### Examples

```bash
# Create TODO list with initial plan
python research.py todos create "WorldString" --priority high \
  --notes "Focus on understanding the neural architecture"

# Add multiple items
python research.py todos add "WorldString" "Read abstract and introduction"
python research.py todos add "WorldString" "Understand the transformer architecture"
python research.py todos add "WorldString" "Study the attention mechanism"
python research.py todos add "WorldString" "Review experimental results"

# As you read, mark items complete
python research.py todos complete "WorldString" 0
python research.py todos complete "WorldString" "transformer"

# Check progress
python research.py todos stats "WorldString"

# List remaining TODOs (hide completed)
python research.py todos list "WorldString" --hide-completed

# View all paper TODOs
python research.py todos list

# Get overview of all papers
python research.py todos stats
```

## Common Workflows

### Workflow 1: Starting a new paper

```bash
# Add the paper
python research.py papers add "https://arxiv.org/abs/1706.03762" --priority high

# Create reading plan
python research.py todos create "Attention Is All You Need" --priority high

# Add reading tasks
python research.py todos add "Attention" "Read abstract and introduction"
python research.py todos add "Attention" "Understand architecture diagrams"
python research.py todos add "Attention" "Work through mathematical details"
python research.py todos add "Attention" "Review experimental setup"
python research.py todos add "Attention" "Note key contributions"
```

### Workflow 2: Progressive reading

```bash
# Check what's next
python research.py todos list "Attention"

# After reading a section
python research.py todos complete "Attention" 0

# Add new tasks as needed
python research.py todos add "Attention" "Implement self-attention in code"

# Check progress
python research.py todos stats "Attention"
```

### Workflow 3: Implementation-focused reading

```bash
# Create implementation-focused TODOs
python research.py todos create "BERT" --priority high
python research.py todos add "BERT" "Understand model architecture"
python research.py todos add "BERT" "Study pretraining tasks"
python research.py todos add "BERT" "Review tokenization approach"
python research.py todos add "BERT" "Implement masked language modeling"
python research.py todos add "BERT" "Implement next sentence prediction"
python research.py todos add "BERT" "Fine-tune on downstream task"
```

### Workflow 4: Survey paper reading

```bash
python research.py todos create "Transformer Survey" --priority medium
python research.py todos add "Transformer Survey" "Read overview and taxonomy"
python research.py todos add "Transformer Survey" "List key papers in each category"
python research.py todos add "Transformer Survey" "Understand evolution timeline"
python research.py todos add "Transformer Survey" "Note comparison methodology"
python research.py todos add "Transformer Survey" "Extract future research directions"
```

## Integration Examples

### With Paper Management Skill

```python
from paper_skill import add_paper_auto
from paper_todo_skill import create_paper_todo

# Combined workflow
def add_paper_with_plan(paper_input, todo_list=None):
    """Add paper and create TODO list in one step"""
    
    # Add the paper
    result = add_paper_auto(paper_input)
    
    if not result['success']:
        return result
    
    # Create default TODO list if none provided
    if todo_list is None:
        todo_list = [
            "Read abstract and introduction",
            "Understand methodology",
            "Review experimental results",
            "Note key contributions"
        ]
    
    # Create TODO list
    todo_result = create_paper_todo(
        result['paper']['title'],
        todos=todo_list,
        priority=result.get('priority', 'medium')
    )
    
    return {
        'paper_result': result,
        'todo_result': todo_result
    }

# Usage
add_paper_with_plan("https://arxiv.org/abs/1706.03762")
```

### Progress Tracking

```python
from paper_todo_skill import get_todo_stats

def get_reading_dashboard():
    """Get overview of all reading progress"""
    
    result = get_todo_stats()
    
    if result['success']:
        stats = result['stats']
        
        # Sort by progress (incomplete papers first)
        in_progress = [s for s in stats if 0 < s['progress'] < 100]
        not_started = [s for s in stats if s['progress'] == 0]
        completed = [s for s in stats if s['progress'] == 100]
        
        return {
            'in_progress': sorted(in_progress, key=lambda x: x['progress'], reverse=True),
            'not_started': not_started,
            'completed': completed
        }

# Usage
dashboard = get_reading_dashboard()
print(f"In Progress: {len(dashboard['in_progress'])}")
print(f"Not Started: {len(dashboard['not_started'])}")
print(f"Completed: {len(dashboard['completed'])}")
```

### Smart TODO Suggestions

```python
from paper_todo_skill import create_paper_todo

def suggest_todos_from_paper(paper_metadata):
    """Generate TODO list based on paper metadata"""
    
    title = paper_metadata['title']
    tags = paper_metadata.get('tags', [])
    
    base_todos = [
        "Read abstract and introduction",
        "Understand methodology",
        "Review results"
    ]
    
    # Add specific tasks based on tags
    if 'cs.CV' in tags or 'computer-vision' in tags:
        base_todos.append("Analyze architecture diagrams")
        base_todos.append("Review dataset and metrics")
    
    if 'cs.LG' in tags or 'deep-learning' in tags:
        base_todos.append("Study training procedure")
        base_todos.append("Note hyperparameters")
    
    if 'implementation' in title.lower():
        base_todos.append("Review code examples")
        base_todos.append("Reproduce key results")
    
    return create_paper_todo(title, todos=base_todos)
```

## Tips for Effective Use

1. **Granular Tasks**: Break down reading into specific, achievable tasks
   - Good: "Understand the multi-head attention mechanism"
   - Bad: "Read the paper"

2. **Implementation Tasks**: Add coding tasks for papers you want to implement
   - "Implement self-attention layer"
   - "Reproduce Table 1 results"

3. **Progressive Refinement**: Add new TODOs as you discover complexity
   - Start with high-level tasks
   - Add detailed tasks as you read

4. **Priority Alignment**: Match TODO priority with paper priority
   - High priority papers → detailed reading plans
   - Low priority papers → quick overview tasks

5. **Regular Reviews**: Check stats regularly to track progress
   ```bash
   python research.py todos stats
   ```

## Future Enhancements

Potential additions:
- **Time estimates**: Add expected time for each task
- **Dependencies**: Mark tasks that depend on others
- **Due dates**: Add deadlines for tasks
- **Tags**: Tag tasks by type (reading, implementation, writing)
- **Notes per task**: Add notes/insights to completed tasks
- **Export**: Export TODO lists to markdown/todo.txt format
- **Templates**: Predefined TODO templates for common paper types
- **Integration**: Auto-create TODOs based on paper abstract analysis

## Contributing

To extend the TODO skill:

1. Add new fields to the TODO data structure in `paper_todo_skill.py`
2. Update the `PaperTodoManager` class methods
3. Add corresponding CLI commands in `research.py`
4. Update documentation

The system is designed to be extensible and integrate seamlessly with other research tools!
