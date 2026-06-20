# ResearchSpace

A personal research organization system for managing papers, notes, and research activities.

## Features

### 📚 Paper Management
Track papers you want to read and papers you've already read with full metadata, notes, and search capabilities.

### 🤖 AI Agent-Friendly Paper Skill
Automatically fetch and organize papers from various sources:
- **arXiv** (URLs or IDs)
- **HuggingFace Papers** (paper links)
- **BibTeX** (paste entire citation)
- **Paper Names** (automatic search)

See [PAPER_SKILL.md](PAPER_SKILL.md) for detailed documentation and agent integration examples.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# 🚀 NEW: Add papers automatically with the Paper Management Skill!
# Just provide an arXiv URL, ID, HuggingFace link, BibTeX, or paper name
python research.py papers add "https://arxiv.org/abs/1706.03762"
python research.py papers add "Attention Is All You Need" --priority high

# Or use the manual method
python research.py papers add-to-read "Paper Title" --authors "Author Name" --url "https://arxiv.org/..."

# Mark a paper as read
python research.py papers mark-read "Paper Title" --notes "Key findings..."

# List papers
python research.py papers list to-read
python research.py papers list read

# Search papers
python research.py papers search "keyword"
```

## Structure

```
ResearchSpace/
├── papers/              # Paper tracking data
│   ├── to_read.json    # Papers in reading queue
│   └── read.json       # Completed papers
├── notes/              # Detailed paper notes and annotations
├── research.py         # Main CLI tool
└── requirements.txt    # Python dependencies
```

## Paper Management Commands

### Adding Papers (Automatic - Recommended! 🚀)
```bash
# Add by arXiv URL - automatically fetches all metadata!
python research.py papers add "https://arxiv.org/abs/1706.03762" --priority high

# Add by arXiv ID
python research.py papers add "1706.03762"

# Add by paper name - searches arXiv automatically!
python research.py papers add "Attention Is All You Need" --tags "must-read"

# Add by HuggingFace paper link
python research.py papers add "https://huggingface.co/papers/2303.08774"

# Preview before adding
python research.py papers add "1706.03762" --preview

# Add directly to read list
python research.py papers add "Attention Is All You Need" --read --rating 5
```

### Adding Papers (Manual)
```bash
# Add to reading list (manual entry)
python research.py papers add-to-read "Attention Is All You Need" \
    --authors "Vaswani et al." \
    --url "https://arxiv.org/abs/1706.03762" \
    --tags "transformers,nlp" \
    --priority high

# Add directly as read (manual entry)
python research.py papers add-read "Paper Title" \
    --authors "Authors" \
    --url "URL" \
    --notes "Summary and insights" \
    --rating 5
```

### Managing Papers
```bash
# Mark paper as read
python research.py papers mark-read "Paper Title" \
    --notes "Key takeaways" \
    --rating 4

# Remove a paper
python research.py papers remove "Paper Title" --from to-read

# Update paper metadata
python research.py papers update "Paper Title" --priority high --tags "new,tags"
```

### Viewing Papers
```bash
# List all papers to read
python research.py papers list to-read

# List read papers
python research.py papers list read

# List with filters
python research.py papers list to-read --priority high
python research.py papers list read --rating 5

# Search across all papers
python research.py papers search "transformer"

# Show detailed info
python research.py papers show "Paper Title"
```

## Data Format

Papers are stored in JSON format with the following schema:

### To-Read Papers
```json
{
  "title": "Paper Title",
  "authors": "Author Names",
  "url": "https://...",
  "added_date": "2026-06-20",
  "priority": "medium",
  "tags": ["tag1", "tag2"],
  "notes": "Initial thoughts"
}
```

### Read Papers
```json
{
  "title": "Paper Title",
  "authors": "Author Names",
  "url": "https://...",
  "added_date": "2026-06-20",
  "read_date": "2026-06-20",
  "rating": 4,
  "tags": ["tag1", "tag2"],
  "summary": "Key findings",
  "notes": "Detailed notes"
}
```

## Future Features

This system is designed to grow with your research needs. Planned features include:
- 📝 Note-taking and annotation system
- 🔗 Citation management
- 📊 Research analytics and insights
- 🗂️ Project organization
- 📅 Research planning and goals
- 🤝 Collaboration tools

## Contributing

This is a personal research space, but feel free to adapt it for your own use!
