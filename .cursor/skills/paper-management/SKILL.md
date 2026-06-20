---
name: paper-management
description: Use this skill when the user asks to add, organize, or manage research papers. Supports arXiv URLs/IDs, HuggingFace paper links, BibTeX entries, and paper names. Automatically fetches metadata including title, authors, abstract, and suggests relevant tags.
---

# Paper Management Skill

This skill helps you automatically add and organize research papers by fetching metadata from various sources.

## When to Use This Skill

Use this skill when the user:
- Provides a paper link (arXiv, HuggingFace)
- Provides a paper ID (e.g., "1706.03762")
- Provides a BibTeX citation
- Asks to add a paper by name
- Wants to organize their research papers
- Requests paper metadata to be fetched automatically

## Supported Input Types

1. **arXiv URLs**: `https://arxiv.org/abs/1706.03762`
2. **arXiv IDs**: `1706.03762`
3. **HuggingFace Paper URLs**: `https://huggingface.co/papers/2303.08774`
4. **BibTeX Entries**: Complete `@article{...}` blocks
5. **Paper Names**: Searches arXiv automatically (e.g., "Attention Is All You Need")

## How to Use

### Python API (Recommended for Agents)

The skill scripts are located in `.cursor/skills/paper-management/scripts/`.

**For Cursor AI Agents**: The skill is automatically available - no imports needed. Just use the functions as documented.

**For Direct Python Usage**:
```python
import sys
sys.path.insert(0, '.cursor/skills/paper-management/scripts')

from paper_skill import add_paper_auto

# Add paper with any input type
result = add_paper_auto(
    input_str="<user's paper input>",
    priority="high",  # or "medium", "low"
    additional_tags=["must-read", "fundamentals"],
    additional_notes="User's notes here"
)

if result['success']:
    # Paper added successfully
    paper = result['paper']
    tags = result['tags']
    # Inform user: Added "{paper['title']}" with tags: {', '.join(tags)}
else:
    # Handle error
    # Inform user: {result['message']}
```

### CLI Method (Alternative)

```bash
# From workspace root
python .cursor/skills/paper-management/scripts/research.py papers add "<paper_url_or_name>" --priority high --tags "tag1,tag2"
```

## Step-by-Step Instructions

### Step 1: Identify the Input Type

The skill automatically detects:
- URLs containing "arxiv.org" → arXiv
- URLs containing "huggingface.co/papers" → HuggingFace
- Text starting with "@article", "@inproceedings", "@misc" → BibTeX
- Numeric pattern like "1234.5678" → arXiv ID
- Everything else → Paper name search

### Step 2: Fetch Metadata

The skill will:
1. Connect to the appropriate source (arXiv API, etc.)
2. Retrieve: title, authors, abstract, publication date, categories
3. Auto-suggest tags based on paper content and categories

### Step 3: Add to Library

The paper is added to the user's reading list with:
- Complete metadata
- Auto-suggested tags (can add more with `additional_tags`)
- Priority level (high/medium/low)
- Notes/summary

### Step 4: Confirm to User

Always inform the user:
- Paper title and authors
- URL for reference
- Tags that were applied
- Priority level set

## Common Patterns

### Pattern 1: User Shares a Link

**User:** "Add this paper: https://arxiv.org/abs/1706.03762"

**Action:**
```python
result = add_paper_auto("https://arxiv.org/abs/1706.03762", priority="medium")
print(f"Added: {result['paper']['title']}")
print(f"Authors: {result['paper']['authors']}")
print(f"Tags: {', '.join(result['tags'])}")
```

### Pattern 2: User Provides BibTeX

**User:** Pastes a BibTeX entry

**Action:**
```python
result = add_paper_auto(user_bibtex_text)
# System automatically detects it's BibTeX and processes accordingly
```

### Pattern 3: User Mentions Paper by Name

**User:** "Add the Attention Is All You Need paper"

**Action:**
```python
result = add_paper_auto("Attention Is All You Need")
# Searches arXiv and adds best match
```

### Pattern 4: Multiple Papers

**User:** "Add these papers: [list of URLs/names]"

**Action:**
```python
papers = ["url1", "url2", "paper name"]
for paper_input in papers:
    result = add_paper_auto(paper_input)
    print(f"{'✓' if result['success'] else '✗'} {result['message']}")
```

## Options

- **priority**: `"high"`, `"medium"` (default), `"low"`
- **additional_tags**: List of strings to add beyond auto-suggested tags
- **additional_notes**: Extra notes to append to the fetched summary
- **mark_as_read**: Boolean, if True adds to read list instead of to-read
- **rating**: Integer 1-5, only used if mark_as_read=True

## Error Handling

Common errors and how to handle them:

1. **Paper not found**: Inform user the paper couldn't be found, suggest using arXiv ID directly
2. **Paper already exists**: Let user know the paper is already in their library
3. **Network timeout**: Inform user there was a connection issue, suggest trying again

## Important Notes

- **Data Directories**: Create `papers/` and `notes/` folders in your workspace with JSON files for data storage
- **Running**: Always run scripts from workspace root using full path to scripts directory
- **Internet**: The skill requires internet access to fetch metadata from arXiv API
- **BibTeX**: BibTeX entries with arXiv URLs will fetch additional metadata from arXiv
- **Tags**: Tag suggestions are automatic but can be extended with `additional_tags`
- **For Agents**: Cursor AI agents automatically have access to this skill - no manual setup required

## Reference Files

See `references/` folder for:
- API documentation
- Tag taxonomy guidelines
- Integration examples

## Examples of Good Usage

✅ **Good**: User provides link → fetch metadata → add to library → confirm with details
✅ **Good**: User provides name → search → preview → confirm → add
✅ **Good**: Multiple papers → process each → report results
✅ **Good**: Ask for priority/tags if user indicates importance

❌ **Avoid**: Adding papers without fetching metadata when source is available
❌ **Avoid**: Ignoring user's priority hints in their message
❌ **Avoid**: Not confirming what was added to the user
