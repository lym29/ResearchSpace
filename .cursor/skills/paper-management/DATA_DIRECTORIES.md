# Data Directories

This document explains how to set up the data directories for paper management.

## Architecture

The ResearchSpace repository contains only the **tools and skills** for managing research papers. Your actual research data (papers and notes) should be stored in a **private repository** to protect your personal information.

## Required Directories

The paper management system expects two directories:

- `paper_management/notes/` - For storing paper notes and annotations
- `paper_management/papers/` - For storing paper metadata JSON files

These directories are `.gitignore`d in the public ResearchSpace repo and should only exist in your private repository.

## Setup Instructions

### Option 1: Using ResearchSpace as a Git Submodule (Recommended)

1. In your private repository (e.g., `ResearchProgress`):
   ```bash
   # Add ResearchSpace as a submodule
   git submodule add https://github.com/lym29/ResearchSpace.git
   
   # Create the data directories in your private repo
   mkdir -p paper_management/notes
   mkdir -p paper_management/papers
   
   # Initialize the required JSON files
   echo "[]" > paper_management/papers/read.json
   echo "[]" > paper_management/papers/to_read.json
   echo "[]" > paper_management/papers/paper_todos.json
   ```

2. The skills from the ResearchSpace submodule can then operate on the data directories in your private repo.

3. Update the submodule when new features are added:
   ```bash
   git submodule update --remote ResearchSpace
   ```

### Option 2: Clone and Create Directories

If not using submodules:

1. Clone ResearchSpace to your local machine
2. Create the directories:
   ```bash
   mkdir -p paper_management/notes
   mkdir -p paper_management/papers
   ```
3. Initialize the JSON files as shown above

## Benefits of This Architecture

- **Privacy**: Your research data stays private
- **Updates**: Get skill improvements from the public repo
- **Separation**: Clear boundary between tools (public) and data (private)
- **Flexibility**: Can use the same skills across multiple private repos

## Example Files

ResearchSpace provides example templates for setting up your private repository:

- `example_private_repo.gitignore` - Example .gitignore for your private repo
- `example_private_repo_README.md` - Example README for your private repo
- `PRIVATE_REPO_GUIDE.md` - Complete setup and usage guide
- `SETUP_PRIVATE_REPO.sh` - Automated setup script

## Notes

- The data directories will be automatically ignored by git in ResearchSpace
- Make sure to back up your private repository regularly
- You can customize the skills in your private repo by creating a fork
- When running scripts, always run from the root of your private repository
