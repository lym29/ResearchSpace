# ResearchSpace

A curated collection of **Cursor AI Skills** for academic research and paper management. These skills work automatically with Cursor AI agents to help you organize, read, and track research papers.

## 🎯 What is ResearchSpace?

ResearchSpace provides AI-ready tools for researchers using Cursor IDE. Instead of running scripts manually, you interact naturally with Cursor AI agents, and they use these skills automatically.

**Example interactions:**
- "Add this paper: https://arxiv.org/abs/1706.03762"
- "Create a reading plan for the Attention Is All You Need paper"
- "Show me all papers tagged with transformers"

## 🚀 Quick Start

### Option 1: Use as Git Submodule (Recommended)

Add ResearchSpace to your research workspace:

```bash
cd your-research-workspace
git submodule add https://github.com/lym29/ResearchSpace.git .cursor/skills/research
```

Cursor will automatically discover and load these skills!

### Option 2: Clone Directly

```bash
git clone https://github.com/lym29/ResearchSpace.git
cd ResearchSpace
```

Open the folder in Cursor, and the skills are ready to use.

### Option 3: Global Skills (All Projects)

Install skills globally for all your Cursor projects:

```bash
git clone https://github.com/lym29/ResearchSpace.git ~/.cursor/skills/research
```

## 📚 Available Skills

### Paper Management (`paper-management`)

Automatically fetch and organize research papers from various sources.

**What it does:**
- Fetches paper metadata from arXiv, HuggingFace, and more
- Auto-suggests relevant tags based on content
- Manages reading lists with priorities
- Creates TODO lists for papers
- Tracks reading progress

**Sources supported:**
- arXiv URLs or IDs
- HuggingFace paper pages
- BibTeX citations
- Paper names (searches automatically)

**Example usage with Cursor AI:**
- "Add the Attention Is All You Need paper to my reading list"
- "I need to read https://arxiv.org/abs/2303.08774, mark it as high priority"
- "Create a TODO list for studying the Transformer paper"
- "Mark the introduction of the Attention paper as complete"

[→ View full skill documentation](.cursor/skills/paper-management/SKILL.md)

## 🏗️ Repository Structure

```
ResearchSpace/
├── .cursor/
│   └── skills/
│       └── paper-management/      # Paper management skill
│           ├── SKILL.md           # Skill definition (auto-loaded by Cursor)
│           ├── scripts/           # Implementation
│           └── references/        # Detailed documentation
├── README.md                      # This file
└── ROADMAP.md                     # Future skills and features
```

## 🔒 Data Privacy

**Important:** This repository contains only the *skills* (tools), not your research data.

Your personal research data (papers, notes, reading progress) should be stored in a **private repository**. ResearchSpace is designed to work as a submodule in your private workspace.

[→ View setup guide](.cursor/skills/paper-management/references/SETUP_GUIDE.md)

## 💡 How Cursor Skills Work

1. **Automatic Discovery**: When you open a workspace, Cursor scans `.cursor/skills/` folders
2. **Context-Aware**: Skills activate automatically based on your conversation
3. **Natural Language**: Just describe what you want - the AI handles the rest
4. **No Manual Setup**: Skills work immediately, no installation required

## 🎓 For Developers

### Using Skills Programmatically

While skills are designed for AI agents, you can also use them directly:

```python
import sys
sys.path.insert(0, '.cursor/skills/paper-management/scripts')

from paper_skill import add_paper_auto

result = add_paper_auto("https://arxiv.org/abs/1706.03762", priority="high")
print(f"Added: {result['paper']['title']}")
```

### CLI Access

```bash
python .cursor/skills/paper-management/scripts/research.py papers add "https://arxiv.org/abs/1706.03762"
```

## 🗺️ Roadmap

Planned skills for researchers:

- **Note-taking and Annotation**: AI-assisted paper notes and highlights
- **Citation Management**: Bibliography generation and citation tracking
- **Literature Review**: Automated literature mapping and gap analysis
- **Research Analytics**: Reading patterns and topic clustering
- **Collaboration**: Share reading lists and notes with team members

[→ View detailed roadmap](ROADMAP.md)

## 🤝 Contributing

ResearchSpace is designed to grow with the research community:

- **Add new skills**: Create skills for your research workflow
- **Improve existing skills**: Enhance paper management features
- **Share feedback**: Report issues or suggest improvements

Each skill is modular and independent, making it easy to contribute!

## 📖 Learn More

- [Paper Management Skill Documentation](.cursor/skills/paper-management/references/README.md)
- [API Reference](.cursor/skills/paper-management/references/api_reference.md)
- [Usage Examples](.cursor/skills/paper-management/references/USAGE_EXAMPLES.md)
- [Cursor Skills Documentation](https://cursor.com/docs/context/skills)

## 📄 License

MIT License - Feel free to use and adapt for your research needs!

---

**Built for researchers using Cursor AI** 🔬 + 🤖
