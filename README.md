# ResearchSpace

A personal research organization system with AI-agent-friendly tools for managing papers, notes, and research activities.

## 🔒 Privacy-First Architecture

ResearchSpace is designed to keep your research data private:

- **This repository contains only the tools and skills** - no personal research data
- **Your data stays in your private repository** - use ResearchSpace as a git submodule
- **Clear separation** - Tools are public, your notes and papers remain private

[→ Learn how to set up with a private repository](.cursor/skills/paper-management/DATA_DIRECTORIES.md)

## 🗂️ Tools

### 📚 Paper Management

Intelligent paper organization system with automatic metadata fetching from arXiv, HuggingFace, BibTeX, and paper name search.

**Structure:**
- **Skill Definition**: `.cursor/skills/paper-management/SKILL.md` - Instructions for AI agents
- **Scripts**: `.cursor/skills/paper-management/scripts/` - Python implementation
- **Documentation**: Available in the scripts folder

**Features:**
- Automatic metadata fetching from multiple sources
- Smart tag suggestions based on paper content
- AI agent-friendly API with Cursor skill integration
- Reading list management with priorities and ratings
- Full-text search across papers
- TODO list management for papers - organize reading tasks and track progress
- Beautiful HTML dashboard for visualizing reading progress

**Quick Start:**
```bash
# Install dependencies (from workspace root)
pip install -r .cursor/skills/paper-management/scripts/requirements.txt

# Add a paper
python .cursor/skills/paper-management/scripts/research.py papers add "https://arxiv.org/abs/1706.03762"

# Create a TODO list for reading
python .cursor/skills/paper-management/scripts/research.py todos create "Attention Is All You Need"

# Generate HTML dashboard
python .cursor/skills/paper-management/scripts/research.py dashboard
# Open reading_progress.html in your browser!
```

[→ View Paper Management Documentation](.cursor/skills/paper-management/scripts/README.md)  
[→ View TODO List Skill Documentation](.cursor/skills/paper-management/scripts/TODO_SKILL_README.md)  
[→ View Cursor Skill Definition](.cursor/skills/paper-management/SKILL.md)

## 🚀 Quick Navigation

- **Cursor Skills**: [`.cursor/skills/`](.cursor/skills/) - AI agent skill definitions
- **Paper Management Scripts**: [`.cursor/skills/paper-management/scripts/`](.cursor/skills/paper-management/scripts/) - Implementation code
- **Roadmap**: [`ROADMAP.md`](ROADMAP.md) - Future features and development plans
- **Setup Guide**: [`.cursor/skills/paper-management/DATA_DIRECTORIES.md`](.cursor/skills/paper-management/DATA_DIRECTORIES.md) - Private repo setup instructions

## 📋 High-Level Goals

- [x] Paper tracking and organization system
- [x] AI agent-friendly paper management skill
- [ ] Note-taking and annotation system
- [ ] Citation management
- [ ] Research analytics and insights
- [ ] Project organization
- [ ] Research planning and goals
- [ ] Collaboration tools

## 🤖 For AI Agents

This repository is designed to be agent-friendly with **Cursor Skills** for automatic discovery:

### 📝 Available Skills (`.cursor/skills/`)

- **`paper-management`** - Add and organize papers from arXiv, HuggingFace, BibTeX, or by name with automatic metadata fetching

**How Skills Work:**
- Skills are automatically discovered by Cursor AI agents
- Agents use skills when relevant based on conversation context
- Skills provide step-by-step instructions and access to scripts

**Example Agent Interactions:**
- "Add this paper: https://arxiv.org/abs/1706.03762"
- "Create a reading plan for the Attention paper"
- "I finished reading the introduction, mark it complete"

### Direct API Usage

The paper management system also provides clean Python APIs for programmatic use:

```python
import sys
sys.path.insert(0, '.cursor/skills/paper-management/scripts')

from paper_skill import add_paper_auto
from paper_todo_skill import create_paper_todo

# Add paper
result = add_paper_auto("https://arxiv.org/abs/1706.03762", priority="high")

# Create TODO list
create_paper_todo(result['paper']['title'], todos=["Read intro", "Understand arch"])
```

**Note**: For AI agents using Cursor, the skill is automatically available - no manual imports needed!

[→ View Skill Documentation](.cursor/skills/paper-management/SKILL.md)

## 📖 Repository Structure

```
ResearchSpace/
├── .cursor/
│   └── skills/
│       └── paper-management/      # Cursor skill for AI agents
│           ├── SKILL.md           # Skill definition and instructions
│           ├── DATA_DIRECTORIES.md # Setup guide for private repos
│           ├── scripts/           # Python implementation
│           │   ├── research.py    # CLI tool
│           │   ├── paper_skill.py # Agent API
│           │   ├── paper_fetcher.py
│           │   ├── generate_dashboard.py
│           │   └── requirements.txt
│           └── references/        # API documentation
├── ROADMAP.md                     # Development plans
└── README.md                      # This file
```

**Note**: Paper data (`papers/`, `notes/`) directories are not included in this repo. See [DATA_DIRECTORIES.md](.cursor/skills/paper-management/DATA_DIRECTORIES.md) for setup instructions.

## 🤝 Contributing

This is a personal research space designed to grow with research needs. Each tool is modular and can be adapted independently.

## 📄 License

MIT License - Feel free to adapt for your own use!
