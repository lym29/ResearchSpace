# Setting Up a Private Repository with ResearchSpace

This guide helps you set up a private repository that uses ResearchSpace as a git submodule, keeping your research tools public while your data stays private.

## Quick Start

### Option 1: Automated Setup

1. Create a new private repository (e.g., `ResearchProgress`)
2. Clone it locally
3. Download and run the setup script:

```bash
cd ResearchProgress
curl -o setup.sh https://raw.githubusercontent.com/lym29/ResearchSpace/main/SETUP_PRIVATE_REPO.sh
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

1. **Create your private repository**
   ```bash
   mkdir ResearchProgress
   cd ResearchProgress
   git init
   ```

2. **Add ResearchSpace as a submodule**
   ```bash
   git submodule add https://github.com/lym29/ResearchSpace.git
   git submodule update --init --recursive
   ```

3. **Create data directories**
   ```bash
   mkdir -p paper_management/notes
   mkdir -p paper_management/papers
   ```

4. **Initialize data files**
   ```bash
   echo "[]" > paper_management/papers/read.json
   echo "[]" > paper_management/papers/to_read.json
   echo "[]" > paper_management/papers/paper_todos.json
   ```

5. **Install dependencies**
   ```bash
   pip install -r ResearchSpace/paper_management/requirements.txt
   ```

6. **Create a convenient symlink** (optional)
   ```bash
   ln -s ResearchSpace/paper_management/research.py research.py
   ```

## Directory Structure

After setup, your private repository should look like this:

```
ResearchProgress/                    # Your private repo
├── .git/
├── .gitignore
├── ResearchSpace/                   # Git submodule (public tools)
│   ├── .cursor/
│   │   └── skills/
│   ├── paper_management/
│   │   ├── research.py
│   │   ├── paper_skill.py
│   │   └── ...
│   └── README.md
├── paper_management/                # Your private data
│   ├── notes/                       # Your paper notes (private)
│   ├── papers/                      # Your paper metadata (private)
│   │   ├── read.json
│   │   ├── to_read.json
│   │   └── paper_todos.json
└── research.py -> ResearchSpace/... # Symlink for convenience
```

## Usage

### Adding Papers

```bash
# Using the symlink
python research.py papers add "https://arxiv.org/abs/1706.03762"

# Or directly
python ResearchSpace/paper_management/research.py papers add "1706.03762"

# Or via Python
cd ResearchSpace/paper_management
python -c "from paper_skill import add_paper_auto; add_paper_auto('1706.03762')"
```

### Managing TODOs

```bash
python research.py todos create "Attention Is All You Need"
python research.py todos add "Attention" "Read the introduction"
python research.py todos complete "Attention" 0
```

### Generating Dashboard

```bash
python research.py dashboard
# Opens reading_progress.html in your browser
```

### Using with Cursor AI

Cursor AI can automatically discover and use the skills:

1. Open your private repository in Cursor
2. The skills in `ResearchSpace/.cursor/skills/` will be automatically available
3. Just ask naturally:
   - "Add this paper: https://arxiv.org/abs/1706.03762"
   - "Create a reading plan for the Attention paper"

## Updating ResearchSpace

To get the latest features and improvements:

```bash
git submodule update --remote ResearchSpace
git add ResearchSpace
git commit -m "Update ResearchSpace submodule"
```

## .gitignore Configuration

Your private repository should **include** the data directories. Create a `.gitignore` that does NOT ignore them:

```gitignore
# Python
__pycache__/
*.pyc
.Python

# IDE
.vscode/
.idea/

# OS
.DS_Store

# IMPORTANT: Don't ignore your research data
# These directories should be tracked in your private repo
!paper_management/notes/
!paper_management/papers/
```

## Benefits of This Setup

### ✅ Privacy
- Your research notes and paper metadata never leave your private repo
- Only the tools are public

### ✅ Updates
- Get new features by updating the submodule
- No need to manually copy scripts

### ✅ Separation
- Clear boundary between tools (public) and data (private)
- Easy to maintain both independently

### ✅ Reusability
- Use the same tools across multiple private research projects
- Each project can have its own private data

### ✅ Collaboration
- Share tools with the community
- Keep your research confidential

## Cursor Skills Integration

The Cursor skills will work automatically when you open your private repository in Cursor:

**Available Skills:**
- `add-research-paper` - Add papers from arXiv, HuggingFace, BibTeX
- `manage-paper-todos` - Create and track reading TODO lists

These skills are defined in `ResearchSpace/.cursor/skills/` and operate on your private data in `paper_management/`.

## Troubleshooting

### Submodule not initialized
```bash
git submodule update --init --recursive
```

### Permission denied when accessing private repo
Make sure you've set up SSH keys or use HTTPS with credentials:
```bash
git config credential.helper store
```

### Scripts can't find data directories
Make sure you're running scripts from the root of your private repo, or use absolute paths:
```bash
cd /path/to/ResearchProgress
python research.py papers add "..."
```

### Python import errors
Install dependencies:
```bash
pip install -r ResearchSpace/paper_management/requirements.txt
```

## Advanced: Multiple Research Projects

You can use ResearchSpace in multiple private repositories:

```bash
# Project 1: NLP Research
mkdir NLP-Research
cd NLP-Research
git init
git submodule add https://github.com/lym29/ResearchSpace.git
# ... create data directories ...

# Project 2: Computer Vision Research
mkdir CV-Research
cd CV-Research
git init
git submodule add https://github.com/lym29/ResearchSpace.git
# ... create data directories ...
```

Each project maintains its own private research data while sharing the same tools.

## Backup Strategy

Since your research data is in a private git repository:

1. **Push regularly**: `git push origin main`
2. **Use private remote**: GitHub, GitLab, or Bitbucket private repos
3. **Optional**: Set up automatic backups to cloud storage
4. **Consider**: Encrypted backups for sensitive research

## Migration from Old Setup

If you previously had data in the public ResearchSpace repo:

1. **Backup your data first**
   ```bash
   cp -r paper_management/notes ~/backup_notes
   cp -r paper_management/papers ~/backup_papers
   ```

2. **Set up private repo** (follow Quick Start above)

3. **Copy your data**
   ```bash
   cp -r ~/backup_notes/* ResearchProgress/paper_management/notes/
   cp -r ~/backup_papers/* ResearchProgress/paper_management/papers/
   ```

4. **Commit to private repo**
   ```bash
   cd ResearchProgress
   git add paper_management/
   git commit -m "Import existing research data"
   git push
   ```

## Questions?

- See full documentation: [ResearchSpace/paper_management/README.md](https://github.com/lym29/ResearchSpace/tree/main/paper_management)
- Report issues: [ResearchSpace Issues](https://github.com/lym29/ResearchSpace/issues)
