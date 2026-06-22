# Paper Management API Reference

## Core Function: add_paper_auto()

Located in: `.cursor/skills/paper-management/scripts/paper_skill.py`

### Signature

```python
def add_paper_auto(
    input_str: str,
    priority: str = "medium",
    additional_tags: List[str] = None,
    additional_notes: str = None,
    mark_as_read: bool = False,
    rating: Optional[int] = None,
    custom_summary: Optional[str] = None
) -> Dict
```

### Parameters

- **input_str** (required): Any supported input format
  - arXiv URL: `https://arxiv.org/abs/1706.03762`
  - arXiv ID: `1706.03762`
  - HuggingFace URL: `https://huggingface.co/papers/2303.08774`
  - BibTeX entry: Complete citation block
  - Paper name: `"Attention Is All You Need"`

- **priority**: Reading priority level
  - `"high"`: Foundational papers, directly relevant to current work
  - `"medium"`: Default, interesting papers
  - `"low"`: Background reading

- **additional_tags**: Extra tags beyond auto-suggested ones
  - Example: `["must-read", "fundamentals", "review-later"]`

- **additional_notes**: Notes to append to fetched summary
  - Example: `"Recommended by colleague, focus on Section 3"`

- **mark_as_read**: If True, adds to read list instead of to-read
  - Default: `False`

- **rating**: Paper rating 1-5 (only used if mark_as_read=True)
  - 5: Exceptional, must-read, foundational
  - 4: Excellent, significant contribution
  - 3: Good, solid work
  - 2: Okay, limited impact
  - 1: Poor, not recommended

- **custom_summary**: Override auto-fetched summary
  - Use when user provides their own summary

### Return Value

```python
{
    'success': bool,           # Whether operation succeeded
    'message': str,            # Human-readable result message
    'paper': dict,             # Paper metadata (if successful)
    'input_type': str,         # 'arxiv', 'bibtex', 'paper_name', 'huggingface'
    'tags': list,              # Final list of applied tags
    'priority': str            # Priority level (if to-read)
}
```

### Paper Metadata Structure

```python
{
    'title': str,              # Full paper title
    'authors': str,            # Comma-separated author list
    'url': str,                # Canonical URL
    'summary': str,            # Abstract (truncated to 500 chars)
    'published_date': str,     # YYYY-MM-DD format
    'tags': list,              # Auto-detected tags from categories
    'source': str              # 'arxiv', 'bibtex', etc.
}
```

## Helper Function: search_and_preview()

Preview paper without adding to library.

```python
def search_and_preview(input_str: str) -> Dict
```

Returns:
```python
{
    'success': bool,
    'message': str,
    'input_type': str,
    'metadata': dict,          # Full paper metadata
    'suggested_tags': list     # Auto-suggested tags
}
```

## Auto-Suggested Tags

Based on arXiv categories and keyword detection:

### Common Tags

- `transformers`, `attention` - Transformer architecture
- `bert`, `nlp`, `pretraining` - NLP models
- `gpt`, `language-models`, `llm` - Language models
- `computer-vision` - Vision tasks
- `deep-learning`, `machine-learning` - General ML
- `reinforcement-learning` - RL papers
- `diffusion-models`, `gan`, `generative` - Generative models
- `multimodal` - Multi-modal models
- `survey` - Survey papers

### arXiv Categories

Common categories that become tags:
- `cs.CL` - Computation and Language
- `cs.CV` - Computer Vision
- `cs.LG` - Machine Learning
- `cs.AI` - Artificial Intelligence
- `stat.ML` - Statistics Machine Learning

## Usage Examples

### Basic Usage

```python
import sys
sys.path.insert(0, '.cursor/skills/paper-management/scripts')

from paper_skill import add_paper_auto

result = add_paper_auto("https://arxiv.org/abs/1706.03762")
```

### With Priority and Tags

```python
result = add_paper_auto(
    "1706.03762",
    priority="high",
    additional_tags=["must-read", "fundamentals"]
)
```

### Mark as Already Read

```python
result = add_paper_auto(
    "Attention Is All You Need",
    mark_as_read=True,
    rating=5,
    additional_notes="Revolutionary paper that changed NLP"
)
```

### Preview Before Adding

```python
import sys
sys.path.insert(0, '.cursor/skills/paper-management/scripts')

from paper_skill import search_and_preview

preview = search_and_preview("1706.03762")
if preview['success']:
    print(f"Title: {preview['metadata']['title']}")
    print(f"Authors: {preview['metadata']['authors']}")
    # User confirms, then add
    result = add_paper_auto("1706.03762")
```

### Batch Processing

```python
papers = [
    "https://arxiv.org/abs/1706.03762",
    "https://arxiv.org/abs/1810.04805",
    "GPT-3 paper"
]

results = []
for paper_input in papers:
    result = add_paper_auto(paper_input, priority="medium")
    results.append(result)
    if result['success']:
        print(f"✓ Added: {result['paper']['title']}")
    else:
        print(f"✗ Error: {result['message']}")
```

## Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| "Could not fetch paper metadata" | Paper not found or API error | Try with arXiv ID directly |
| "Paper already exists" | Duplicate paper | Use update command instead |
| "The read operation timed out" | Network timeout | Retry the operation |

## Integration Tips

### For Agents

1. Always use the Python API, not CLI commands
2. Import from `.cursor/skills/paper-management/scripts/` (add to sys.path first)
3. Handle both success and error cases
4. Provide user feedback with paper details
5. Infer priority from user's language ("important" → high, "interesting" → medium)

### For CLI Users

```bash
python .cursor/skills/paper-management/scripts/research.py papers add "<input>" --priority high --tags "tag1,tag2"
python .cursor/skills/paper-management/scripts/research.py dashboard   # static snapshot
python .cursor/skills/paper-management/scripts/research.py serve       # interactive web UI
```

## File Locations

- Main tool: `.cursor/skills/paper-management/scripts/research.py`
- Skill API: `.cursor/skills/paper-management/scripts/paper_skill.py`
- Metadata fetcher: `.cursor/skills/paper-management/scripts/paper_fetcher.py`
- Interactive dashboard server: `.cursor/skills/paper-management/scripts/dashboard_server.py`
- Static dashboard generator: `.cursor/skills/paper-management/scripts/generate_dashboard.py`
- Paper data: User's workspace — `papers/to_read.json`, `papers/read.json`, `papers/paper_todos.json`
- Static dashboard output: `reading_progress.html` (read-only snapshot)
- Dependencies: `.cursor/skills/paper-management/scripts/requirements.txt`
