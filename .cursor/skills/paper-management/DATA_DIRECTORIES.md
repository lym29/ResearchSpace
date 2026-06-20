# Data Storage Configuration

This document explains how to configure data storage for the paper management skill.

## Overview

The paper management skill stores your research data (paper metadata, notes, reading progress) in JSON files on your local filesystem. **You choose where to store this data** - it can be anywhere on your system.

## Default Location

By default, the skill looks for data files in these locations relative to where you run the scripts:

```
your-workspace/
├── papers/
│   ├── read.json           # Papers you've finished reading
│   ├── to_read.json        # Papers in your reading queue
│   └── paper_todos.json    # TODO lists for papers
└── notes/
    └── [your paper notes]  # Notes and annotations
```

## Quick Setup

### Option 1: Use Default Locations

Create the data directories in your workspace:

```bash
mkdir -p papers notes

# Initialize the required JSON files
echo "[]" > papers/read.json
echo "[]" > papers/to_read.json
echo "[]" > papers/paper_todos.json
```

That's it! The skill will now work in your workspace.

### Option 2: Custom Locations (Coming Soon)

In a future update, you'll be able to configure custom paths via environment variables:

```bash
export RESEARCH_PAPERS_DIR="/path/to/my/papers"
export RESEARCH_NOTES_DIR="/path/to/my/notes"
```

## Storage Recommendations

### Keep Your Data Private

Your research data is yours alone. We recommend:

- Store data in a **private Git repository** (separate from this public skills repo)
- Use **git submodules** to include ResearchSpace skills in your private workspace
- Add data directories to your `.gitignore` if you don't want to version them

### Backup Your Data

Since your research data is stored as JSON files:

- ✅ Easy to back up with any backup tool
- ✅ Can version control with Git
- ✅ Portable across machines
- ✅ Human-readable format

### Organize Your Workspace

**Recommended structure:**

```
my-research-workspace/          # Your private repository
├── .cursor/
│   └── skills/
│       └── research/           # ResearchSpace as submodule
├── papers/                     # Your paper data
├── notes/                      # Your notes
├── projects/                   # Your research projects
└── .gitignore                  # Ignore or track data as you prefer
```

## Working with Git Submodules

### Add ResearchSpace to Your Workspace

```bash
cd your-research-workspace
git submodule add https://github.com/lym29/ResearchSpace.git .cursor/skills/research

# Set up data directories
mkdir -p papers notes
echo "[]" > papers/read.json
echo "[]" > papers/to_read.json  
echo "[]" > papers/paper_todos.json

# Commit the structure
git add .
git commit -m "Add ResearchSpace skills and initialize data directories"
```

### Update Skills to Latest Version

```bash
git submodule update --remote .cursor/skills/research
git commit -am "Update ResearchSpace skills"
```

## Data File Formats

### papers/to_read.json
```json
[
  {
    "title": "Attention Is All You Need",
    "authors": "Vaswani et al.",
    "url": "https://arxiv.org/abs/1706.03762",
    "summary": "Paper abstract...",
    "tags": ["transformers", "nlp"],
    "priority": "high",
    "added_date": "2024-01-15"
  }
]
```

### papers/read.json
```json
[
  {
    "title": "BERT: Pre-training of Deep Bidirectional Transformers",
    "authors": "Devlin et al.",
    "url": "https://arxiv.org/abs/1810.04805",
    "summary": "Paper abstract...",
    "tags": ["bert", "nlp", "pretraining"],
    "rating": 5,
    "read_date": "2024-01-20",
    "notes": "Revolutionary approach to pretraining..."
  }
]
```

### papers/paper_todos.json
```json
[
  {
    "paper_title": "Attention Is All You Need",
    "todos": [
      {
        "task": "Read introduction and motivation",
        "completed": true,
        "completed_date": "2024-01-16"
      },
      {
        "task": "Understand multi-head attention mechanism",
        "completed": false
      }
    ],
    "created_date": "2024-01-15"
  }
]
```

## Troubleshooting

### "File not found" errors

Make sure you're running commands from your workspace root where the `papers/` and `notes/` directories exist.

### Data not persisting

Check that JSON files are properly initialized and have write permissions:

```bash
ls -la papers/
# Should show read.json, to_read.json, paper_todos.json
```

### Working across machines

To sync your research data across devices:

1. Store your workspace in a Git repository
2. Commit and push your data files
3. Pull on other machines

Or use cloud sync (Dropbox, Google Drive, etc.) for automatic syncing.

## Example Templates

The references folder includes helpful templates:

- `example_private_repo.gitignore` - Sample .gitignore for your research workspace
- `example_private_repo_README.md` - Template README for your workspace
- `PRIVATE_REPO_GUIDE.md` - Detailed guide for setting up a private repository
- `SETUP_PRIVATE_REPO.sh` - Automated setup script

## Need Help?

See the [complete skill documentation](SKILL.md) or [API reference](references/api_reference.md) for more information.
