# ResearchProgress (Example Private Repository)

This is an example README for a private research repository that uses ResearchSpace as a submodule.

## Overview

This private repository contains my personal research notes, papers, and reading progress. It uses [ResearchSpace](https://github.com/lym29/ResearchSpace) as a git submodule to access research management tools while keeping my data private.

## Structure

```
.
├── README.md                        # This file
├── .gitignore                       # Tracks data directories (unlike public repo)
├── ResearchSpace/                   # Git submodule (public tools)
│   ├── .cursor/skills/              # AI agent skills
│   ├── paper_management/            # Paper management tools
│   └── README.md
├── paper_management/                # My private research data
│   ├── notes/                       # Paper notes and annotations
│   │   └── ...                      # (private, tracked in this repo)
│   └── papers/                      # Paper metadata
│       ├── read.json                # Papers I've finished
│       ├── to_read.json             # Reading list
│       └── paper_todos.json         # Reading tasks
├── research.py -> ResearchSpace/... # Convenience symlink
└── dashboard.html                   # Generated reading dashboard
```

## Quick Commands

### Add a Paper
```bash
python research.py papers add "https://arxiv.org/abs/1706.03762"
python research.py papers add "Attention Is All You Need" --priority high
```

### Manage Reading TODOs
```bash
# Create TODO list for a paper
python research.py todos create "Attention Is All You Need"

# Add tasks
python research.py todos add "Attention" "Read the introduction"
python research.py todos add "Attention" "Understand the architecture"

# Complete tasks
python research.py todos complete "Attention" 0

# View progress
python research.py todos list "Attention"
```

### Generate Dashboard
```bash
python research.py dashboard
# Opens reading_progress.html in your browser
```

### Search Papers
```bash
python research.py papers search "transformer"
python research.py papers list --status to_read
python research.py papers list --status read --rating 5
```

## Using with Cursor AI

When you open this repository in Cursor, the AI can automatically discover and use the skills from the ResearchSpace submodule:

**Example prompts:**
- "Add this paper: https://arxiv.org/abs/1706.03762"
- "Create a reading plan for the Attention Is All You Need paper"
- "Mark the introduction as complete for the Attention paper"
- "Show me all papers tagged with 'transformers'"

## Updating ResearchSpace Tools

To get the latest features and bug fixes:

```bash
git submodule update --remote ResearchSpace
git add ResearchSpace
git commit -m "Update ResearchSpace to latest version"
git push
```

## Backup

This repository is backed up to:
- **Primary**: GitHub private repository
- **Secondary**: [Add your backup location]

Backup frequency: [Add your backup schedule]

## Research Areas

My current research interests:
- [Add your research areas]
- [Add topics you're tracking]

## Statistics

<!-- You can add stats here, or generate them with scripts -->
- Papers tracked: [Generated automatically]
- Papers read: [Generated automatically]
- Current reading: [Generated automatically]

## Notes

- All research data in this repository is **private and confidential**
- The ResearchSpace submodule is public (only contains tools, no data)
- Notes are stored in `paper_management/notes/` in Markdown format
- Paper metadata is stored in `paper_management/papers/*.json`

## Setup (for reference)

This repository was set up using:

```bash
git init
git submodule add https://github.com/lym29/ResearchSpace.git
mkdir -p paper_management/notes paper_management/papers
echo "[]" > paper_management/papers/read.json
echo "[]" > paper_management/papers/to_read.json
echo "[]" > paper_management/papers/paper_todos.json
pip install -r ResearchSpace/paper_management/requirements.txt
ln -s ResearchSpace/paper_management/research.py research.py
```

For detailed setup instructions, see [ResearchSpace/PRIVATE_REPO_GUIDE.md](ResearchSpace/PRIVATE_REPO_GUIDE.md).

## License

This private repository and its contents are **not licensed for public use**. All notes, annotations, and data are personal and confidential.

The ResearchSpace tools (submodule) are licensed under MIT - see [ResearchSpace/LICENSE](ResearchSpace/LICENSE).
