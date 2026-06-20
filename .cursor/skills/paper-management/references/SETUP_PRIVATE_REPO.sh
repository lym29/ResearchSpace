#!/bin/bash
# Setup script for using ResearchSpace as a submodule in a private repository
# Usage: Run this script from the root of your private research repository

set -e

echo "🔧 Setting up ResearchSpace in private repository..."

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo "❌ Error: Not in a git repository. Please run this from your private repo root."
    exit 1
fi

# Add ResearchSpace as a submodule (if not already added)
if [ ! -d ResearchSpace ]; then
    echo "📦 Adding ResearchSpace as a git submodule..."
    git submodule add https://github.com/lym29/ResearchSpace.git
    git submodule update --init --recursive
else
    echo "✓ ResearchSpace submodule already exists"
fi

# Create data directories
echo "📁 Creating data directories..."
mkdir -p paper_management/notes
mkdir -p paper_management/papers

# Initialize JSON data files if they don't exist
if [ ! -f paper_management/papers/read.json ]; then
    echo "[]" > paper_management/papers/read.json
    echo "✓ Created paper_management/papers/read.json"
fi

if [ ! -f paper_management/papers/to_read.json ]; then
    echo "[]" > paper_management/papers/to_read.json
    echo "✓ Created paper_management/papers/to_read.json"
fi

if [ ! -f paper_management/papers/paper_todos.json ]; then
    echo "[]" > paper_management/papers/paper_todos.json
    echo "✓ Created paper_management/papers/paper_todos.json"
fi

# Create .gitignore if it doesn't exist
if [ ! -f .gitignore ]; then
    touch .gitignore
fi

# Ensure the data directories are NOT ignored in the private repo
echo ""
echo "📝 Updating .gitignore..."
echo "# Your private research data - KEEP these in private repo" >> .gitignore
echo "# (ResearchSpace ignores these, but your private repo should NOT)" >> .gitignore
echo "!paper_management/notes/" >> .gitignore
echo "!paper_management/papers/" >> .gitignore

# Create a symlink to the ResearchSpace scripts (optional)
if [ ! -L research.py ]; then
    echo "🔗 Creating symlink to research.py..."
    ln -s ResearchSpace/paper_management/research.py research.py
    echo "✓ You can now run: python research.py"
fi

# Install Python dependencies
if command -v pip &> /dev/null; then
    echo ""
    echo "📦 Installing Python dependencies..."
    pip install -r ResearchSpace/paper_management/requirements.txt
    echo "✓ Dependencies installed"
else
    echo "⚠️  pip not found. Please install dependencies manually:"
    echo "   pip install -r ResearchSpace/paper_management/requirements.txt"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📚 Next steps:"
echo "   1. Add papers: python research.py papers add <arxiv_url>"
echo "   2. Create todos: python research.py todos create <paper_title>"
echo "   3. Generate dashboard: python research.py dashboard"
echo ""
echo "📖 Documentation: ResearchSpace/paper_management/README.md"
echo "🔄 Update ResearchSpace: git submodule update --remote ResearchSpace"
