# ResearchSpace

A personal research organization system with AI-agent-friendly tools for managing papers, notes, and research activities.

## 🗂️ Tools

### 📚 [Paper Management](paper_management/)
Intelligent paper organization system with automatic metadata fetching from arXiv, HuggingFace, BibTeX, and paper name search.

**Features:**
- Automatic metadata fetching from multiple sources
- Smart tag suggestions based on paper content
- AI agent-friendly API
- Reading list management with priorities and ratings
- Full-text search across papers

**Quick Start:**
```bash
cd paper_management
pip install -r requirements.txt
python research.py papers add "https://arxiv.org/abs/1706.03762"
```

[→ View Paper Management Documentation](paper_management/README.md)

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

This repository is designed to be agent-friendly. Each tool provides:
- Clean, documented Python APIs
- CLI interfaces for quick operations
- Comprehensive documentation with usage examples
- Standardized error handling

**Example - Paper Management Skill:**
```python
from paper_management.paper_skill import add_paper_auto

# User says: "Add this paper: https://arxiv.org/abs/1706.03762"
result = add_paper_auto("https://arxiv.org/abs/1706.03762", priority="high")

if result['success']:
    print(f"Added: {result['paper']['title']}")
```

## 📖 Documentation Structure

Each tool has its own folder with:
- `README.md` - Complete documentation and API reference
- `requirements.txt` - Tool-specific dependencies
- Usage examples and integration guides

## 🤝 Contributing

This is a personal research space designed to grow with research needs. Each tool is modular and can be adapted independently.

## 📄 License

MIT License - Feel free to adapt for your own use!
