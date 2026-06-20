# ResearchSpace

A personal research organization system with AI-agent-friendly tools for managing papers, notes, and research activities.

## 🔒 Privacy-First Architecture

ResearchSpace is designed to keep your research data private:

- **This repository contains only the tools and skills** - no personal research data
- **Your data stays in your private repository** - use ResearchSpace as a git submodule
- **Clear separation** - Tools are public, your notes and papers remain private

[→ Learn how to set up with a private repository](paper_management/DATA_DIRECTORIES.md)

## 🗂️ Tools

### 📚 [Paper Management](paper_management/)
Intelligent paper organization system with automatic metadata fetching from arXiv, HuggingFace, BibTeX, and paper name search.

**Features:**
- Automatic metadata fetching from multiple sources
- Smart tag suggestions based on paper content
- AI agent-friendly API
- Reading list management with priorities and ratings
- Full-text search across papers
- TODO list management for papers - organize reading tasks and track progress
- **NEW:** Beautiful HTML dashboard for visualizing reading progress

**Quick Start:**
```bash
cd paper_management
pip install -r requirements.txt

# Add a paper
python research.py papers add "https://arxiv.org/abs/1706.03762"

# Create a TODO list for reading
python research.py todos create "Attention Is All You Need"
python research.py todos add "Attention" "Read the introduction"
python research.py todos complete "Attention" 0

# Generate HTML dashboard
python research.py dashboard
# Open reading_progress.html in your browser!
```

[→ View Paper Management Documentation](paper_management/README.md)  
[→ View TODO List Skill Documentation](paper_management/TODO_SKILL_README.md)

## 🚀 Quick Navigation

- **Paper Management**: [`paper_management/`](paper_management/) - Track and organize research papers
- **Roadmap**: [`ROADMAP.md`](ROADMAP.md) - Future features and development plans

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

- **`add-research-paper`** - Add papers from arXiv, HuggingFace, BibTeX, or by name
- **`manage-paper-todos`** - Create and track reading TODO lists for papers

Agents can discover and use these skills automatically! Just ask naturally:
- "Add this paper: https://arxiv.org/abs/1706.03762"
- "Create a reading plan for the Attention paper"
- "I finished reading the introduction, mark it complete"

### Direct API Usage

Each tool also provides clean Python APIs:
```python
from paper_management.paper_skill import add_paper_auto
from paper_management.paper_todo_skill import create_paper_todo

# Add paper
result = add_paper_auto("https://arxiv.org/abs/1706.03762", priority="high")

# Create TODO list
create_paper_todo(result['paper']['title'], todos=["Read intro", "Understand arch"])
```

[→ View Cursor Skills Documentation](CURSOR_SKILLS_README.md)

## 📖 Documentation Structure

Each tool has its own folder with:
- `README.md` - Complete documentation and API reference
- `requirements.txt` - Tool-specific dependencies
- Usage examples and integration guides

## 🤝 Contributing

This is a personal research space designed to grow with research needs. Each tool is modular and can be adapted independently.

## 📄 License

MIT License - Feel free to adapt for your own use!
