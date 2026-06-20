# Paper Management Skill

An agent-friendly paper management system that automatically fetches and organizes research papers from various sources.

## Overview

The Paper Management Skill transforms paper organization from a manual process into an automated workflow. Simply provide any of the following, and the system will automatically fetch metadata, suggest tags, and organize the paper:

- **arXiv URLs** (`https://arxiv.org/abs/1706.03762`)
- **arXiv IDs** (`1706.03762`)
- **HuggingFace Paper Links** (`https://huggingface.co/papers/2303.08774`)
- **BibTeX Entries** (complete citation blocks)
- **Paper Names** (searches arXiv automatically)

## For AI Agents

### Quick Start

```python
from paper_skill import add_paper_auto

# Add a paper from any source
result = add_paper_auto("https://arxiv.org/abs/1706.03762")

if result['success']:
    print(f"Added: {result['paper']['title']}")
    print(f"Tags: {', '.join(result['tags'])}")
else:
    print(f"Error: {result['message']}")
```

### Agent Usage Patterns

#### Pattern 1: User provides a link

```python
from paper_skill import add_paper_auto

# User says: "Add this paper: https://arxiv.org/abs/1706.03762"
result = add_paper_auto(
    "https://arxiv.org/abs/1706.03762",
    priority="high"  # You can infer priority from user's enthusiasm
)
```

#### Pattern 2: User provides just a paper name

```python
from paper_skill import add_paper_auto

# User says: "Add the Attention Is All You Need paper"
result = add_paper_auto(
    "Attention Is All You Need",
    priority="medium"
)
```

#### Pattern 3: User provides BibTeX

```python
from paper_skill import add_paper_auto

# User pastes a BibTeX entry
bibtex = '''
@article{vaswani2017attention,
  title={Attention is all you need},
  author={Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and others},
  journal={Advances in neural information processing systems},
  year={2017}
}
'''

result = add_paper_auto(bibtex)
```

#### Pattern 4: Add multiple papers

```python
from paper_skill import add_paper_auto

papers = [
    "https://arxiv.org/abs/1706.03762",
    "https://arxiv.org/abs/1810.04805",
    "BERT pretraining paper"
]

for paper_input in papers:
    result = add_paper_auto(paper_input)
    print(f"{'✓' if result['success'] else '✗'} {result['message']}")
```

#### Pattern 5: Preview before adding

```python
from paper_skill import search_and_preview, add_paper_auto

# First, preview the paper
preview = search_and_preview("Attention Is All You Need")

if preview['success']:
    print(f"Found: {preview['metadata']['title']}")
    print(f"Authors: {preview['metadata']['authors']}")
    print(f"Suggested tags: {', '.join(preview['suggested_tags'])}")
    
    # User confirms, then add it
    result = add_paper_auto("Attention Is All You Need", priority="high")
```

### API Reference

#### `add_paper_auto(input_str, **options)`

Automatically fetch and add a paper to the research library.

**Parameters:**
- `input_str` (str, required): Any supported input type
  - arXiv URL or ID
  - HuggingFace paper URL
  - BibTeX entry
  - Paper name
  
- `priority` (str, optional): Priority level - `"low"`, `"medium"` (default), or `"high"`

- `additional_tags` (list, optional): Extra tags beyond auto-suggested ones
  - Example: `["must-read", "fundamentals"]`

- `additional_notes` (str, optional): Extra notes to append

- `mark_as_read` (bool, optional): If `True`, add to read list instead of to-read

- `rating` (int, optional): Rating 1-5 (only if `mark_as_read=True`)

- `custom_summary` (str, optional): Override auto-fetched summary

**Returns:**
```python
{
    'success': bool,           # Whether operation succeeded
    'message': str,            # Human-readable result
    'paper': dict,             # Paper metadata (if successful)
    'input_type': str,         # Type detected: 'arxiv', 'bibtex', 'paper_name'
    'tags': list,              # Final tag list
    'priority': str            # Priority level (if to-read)
}
```

#### `search_and_preview(input_str)`

Preview paper metadata without adding to library.

**Returns:**
```python
{
    'success': bool,
    'message': str,
    'input_type': str,
    'metadata': dict,          # Full paper metadata
    'suggested_tags': list     # Auto-suggested tags
}
```

### Metadata Structure

When papers are fetched, they include:

```python
{
    'title': str,              # Full paper title
    'authors': str,            # Comma-separated author list
    'url': str,                # Canonical URL (arXiv link)
    'summary': str,            # Abstract/summary (truncated to 500 chars)
    'published_date': str,     # Publication date (YYYY-MM-DD)
    'tags': list,              # Auto-detected tags from categories
    'source': str              # Source: 'arxiv', 'bibtex', etc.
}
```

### Tag Suggestions

The system automatically suggests tags based on:
- arXiv categories
- Keywords in title
- Keywords in abstract

Common auto-suggested tags:
- `transformers`, `attention`
- `nlp`, `computer-vision`
- `deep-learning`, `machine-learning`
- `reinforcement-learning`
- `diffusion-models`, `gan`, `generative`
- `llm`, `language-models`
- `multimodal`
- `survey`

### Error Handling

```python
from paper_skill import add_paper_auto

result = add_paper_auto("some-invalid-input")

if not result['success']:
    # Handle error
    if "Could not fetch" in result['message']:
        print("Paper not found or unavailable")
    elif "already exists" in result['message']:
        print("Paper is already in your library")
```

## For Human Users (CLI)

### Basic Usage

```bash
# Add paper by arXiv URL
python research.py papers add "https://arxiv.org/abs/1706.03762"

# Add paper by arXiv ID
python research.py papers add "1706.03762" --priority high

# Add paper by name (searches arXiv)
python research.py papers add "Attention Is All You Need" --tags "must-read"

# Preview before adding
python research.py papers add "1706.03762" --preview
```

### CLI Options

```bash
--priority, -p    Set priority: low, medium (default), high
--tags, -t        Additional comma-separated tags
--notes, -n       Additional notes
--read, -r        Add to read list instead of to-read
--rating          Rating 1-5 (only with --read)
--preview         Preview paper info without adding
```

### Examples

```bash
# High priority paper with custom tags
python research.py papers add "1706.03762" \
    --priority high \
    --tags "transformers,must-read,fundamentals"

# Add and mark as read
python research.py papers add "Attention Is All You Need" \
    --read \
    --rating 5 \
    --notes "Revolutionary paper that changed NLP"

# Preview first
python research.py papers add "BERT pretraining" --preview
# Then add if desired
python research.py papers add "BERT pretraining" --priority high
```

### Using Python API directly

```bash
# Use as standalone script
python paper_skill.py "https://arxiv.org/abs/1706.03762"
python paper_skill.py "Attention Is All You Need"
```

## Supported Sources

### arXiv

- **URL formats**: 
  - `https://arxiv.org/abs/1706.03762`
  - `https://arxiv.org/pdf/1706.03762.pdf`
  - `http://arxiv.org/abs/1706.03762`
  
- **ID formats**:
  - `1706.03762` (without version)
  - `1706.03762v1` (with version)

- **Fetched data**: Title, authors, abstract, categories, publication date

### HuggingFace Papers

- **URL format**: `https://huggingface.co/papers/2303.08774`
- **Note**: HuggingFace papers use arXiv IDs, so fetches from arXiv API

### BibTeX

- **Supported entry types**: `@article`, `@inproceedings`, `@misc`
- **Required fields**: `title`
- **Optional fields**: `author`, `url`, `year`
- **Note**: If BibTeX contains arXiv URL, will fetch additional metadata from arXiv

### Paper Name Search

- **How it works**: Searches arXiv by title
- **Returns**: Best matching paper
- **Tip**: Use distinctive parts of the title for best results

## Integration Examples

### Slack Bot Integration

```python
# When user sends a message in #paper-reading channel
@bot.message("paper")
def handle_paper(message):
    user_input = message.text
    
    # Check if it looks like a paper link or name
    if "arxiv.org" in user_input or "huggingface.co" in user_input:
        from paper_skill import add_paper_auto
        result = add_paper_auto(user_input)
        
        if result['success']:
            bot.reply(f"✓ Added: {result['paper']['title']}")
        else:
            bot.reply(f"✗ {result['message']}")
```

### Email Integration

```python
# When receiving email with paper links
import re
from paper_skill import add_paper_auto

def process_email(email_body):
    # Find arXiv links
    arxiv_pattern = r'https?://arxiv\.org/abs/[\d\.]+'
    links = re.findall(arxiv_pattern, email_body)
    
    for link in links:
        result = add_paper_auto(link, priority="medium")
        print(f"Added: {result['paper']['title']}")
```

### Browser Extension Integration

```python
# When user clicks "Add to Research" on arXiv page
def add_current_paper(url):
    from paper_skill import add_paper_auto
    return add_paper_auto(url, priority="high")
```

## Advanced Features

### Custom Tag Strategy

```python
from paper_skill import add_paper_auto

# Define your own tag taxonomy
def add_with_custom_tags(paper_input, research_area):
    area_tags = {
        'nlp': ['nlp', 'language'],
        'vision': ['computer-vision', 'image'],
        'rl': ['reinforcement-learning', 'agents']
    }
    
    result = add_paper_auto(
        paper_input,
        additional_tags=area_tags.get(research_area, [])
    )
    
    return result

# Usage
add_with_custom_tags("1706.03762", "nlp")
```

### Batch Processing

```python
from paper_skill import add_paper_auto

def batch_add_papers(paper_list, priority="medium"):
    """Add multiple papers at once"""
    results = []
    
    for paper_input in paper_list:
        result = add_paper_auto(paper_input, priority=priority)
        results.append(result)
        
        if result['success']:
            print(f"✓ {result['paper']['title'][:60]}...")
        else:
            print(f"✗ {result['message']}")
    
    success_count = sum(1 for r in results if r['success'])
    print(f"\nAdded {success_count}/{len(paper_list)} papers")
    
    return results

# Usage
papers = [
    "https://arxiv.org/abs/1706.03762",
    "https://arxiv.org/abs/1810.04805",
    "GPT-3 paper"
]
batch_add_papers(papers, priority="high")
```

### Smart Priority Detection

```python
from paper_skill import add_paper_auto

def smart_add(paper_input, user_message):
    """Infer priority from user's message"""
    
    # Detect urgency keywords
    urgent_words = ['important', 'must read', 'urgent', 'asap', 'critical']
    interested_words = ['interesting', 'cool', 'neat', 'check out']
    
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in urgent_words):
        priority = "high"
    elif any(word in message_lower for word in interested_words):
        priority = "medium"
    else:
        priority = "low"
    
    return add_paper_auto(paper_input, priority=priority)

# Usage
smart_add("1706.03762", "This is a critical paper I must read!")  # → high priority
smart_add("1810.04805", "Interesting BERT paper")  # → medium priority
```

## Troubleshooting

### Paper Not Found

If a paper name search fails:
- Try using the arXiv ID directly
- Use a more specific/distinctive part of the title
- Check if the paper is actually on arXiv

### Network Issues

The system requires internet access to fetch metadata:
- arXiv API: `http://export.arxiv.org/api/`
- Ensure firewall allows outbound HTTP connections

### Duplicate Papers

If a paper already exists:
- Use `papers search` to find existing paper
- Use `papers update` to modify existing paper metadata
- Remove old version with `papers remove` if needed

## Future Enhancements

Potential additions:
- **More sources**: PubMed, Semantic Scholar, Google Scholar
- **PDF download**: Automatically download PDFs
- **Citation extraction**: Parse citations from papers
- **Related papers**: Suggest related papers based on citations
- **Export formats**: BibTeX export, Markdown notes generation
- **Collaboration**: Share reading lists with others

## Contributing

To add support for new sources:

1. Add fetcher function in `paper_fetcher.py`:
   ```python
   def fetch_newsource_metadata(identifier: str) -> Optional[Dict]:
       # Fetch and return standardized metadata
       pass
   ```

2. Update `detect_input_type()` to recognize new source

3. Update `fetch_paper_metadata()` to handle new type

The system will automatically work with all existing integrations!
