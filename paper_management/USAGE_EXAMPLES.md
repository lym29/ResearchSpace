# Usage Examples

## Quick Start Guide

### 1. Installing Dependencies

```bash
pip install -r requirements.txt
```

### 2. Adding Your First Paper

Add a paper you want to read:

```bash
python3 research.py papers add-to-read "Attention Is All You Need" \
    --authors "Vaswani et al." \
    --url "https://arxiv.org/abs/1706.03762" \
    --tags "transformers,nlp,deep-learning" \
    --priority high \
    --notes "Foundation paper for Transformer architecture"
```

### 3. Viewing Your Reading List

```bash
python3 research.py papers list to-read
```

### 4. Marking a Paper as Read

After reading the paper:

```bash
python3 research.py papers mark-read "Attention Is All You Need" \
    --rating 5 \
    --summary "Introduced self-attention mechanism that revolutionized NLP" \
    --notes "Key insights: eliminates recurrence, enables parallelization, scales well"
```

### 5. View Your Read Papers

```bash
python3 research.py papers list read
```

## Common Workflows

### Building a Reading Queue

Add multiple papers to your reading list:

```bash
# High priority - foundational papers
python3 research.py papers add-to-read "BERT: Pre-training of Deep Bidirectional Transformers" \
    --authors "Devlin et al." \
    --url "https://arxiv.org/abs/1810.04805" \
    --tags "nlp,pretraining,transformers" \
    --priority high

# Medium priority - interesting applications
python3 research.py papers add-to-read "GPT-3: Language Models are Few-Shot Learners" \
    --authors "Brown et al." \
    --url "https://arxiv.org/abs/2005.14165" \
    --tags "nlp,language-models,few-shot" \
    --priority medium

# Low priority - background reading
python3 research.py papers add-to-read "A Survey of Large Language Models" \
    --authors "Zhao et al." \
    --tags "survey,llm,nlp" \
    --priority low
```

### Organizing by Priority

View only high-priority papers:

```bash
python3 research.py papers list to-read --priority high
```

### Tracking Your Progress

Check your statistics:

```bash
python3 research.py papers stats
```

### Finding Papers Later

Search across all papers:

```bash
# Search by keyword
python3 research.py papers search "transformer"

# Search by author
python3 research.py papers search "Vaswani"

# Search by tag
python3 research.py papers search "nlp"
```

### Getting Detailed Information

View complete information about a paper:

```bash
python3 research.py papers show "Attention Is All You Need"
```

### Managing Your Library

Update paper metadata:

```bash
python3 research.py papers update "BERT: Pre-training of Deep Bidirectional Transformers" \
    --priority high \
    --tags "nlp,pretraining,transformers,must-read"
```

Remove a paper:

```bash
python3 research.py papers remove "Paper Title" --from to-read
```

### Advanced: Direct Read Entry

If you've already read a paper and want to add it directly:

```bash
python3 research.py papers add-read "AlexNet Paper" \
    --authors "Krizhevsky et al." \
    --url "https://papers.nips.cc/..." \
    --rating 5 \
    --tags "computer-vision,deep-learning,cnn" \
    --summary "Breakthrough CNN for ImageNet, started deep learning revolution" \
    --notes "Key contributions: ReLU, dropout, data augmentation"
```

### Filtering and Organization

View only 5-star papers:

```bash
python3 research.py papers list read --rating 5
```

View papers by tag:

```bash
python3 research.py papers list to-read --tag nlp
```

## Tips and Best Practices

### Tagging Strategy

Use consistent, hierarchical tags:
- **Field**: `nlp`, `computer-vision`, `robotics`
- **Topic**: `transformers`, `reinforcement-learning`, `gan`
- **Type**: `survey`, `tutorial`, `foundation`, `application`
- **Status**: `must-read`, `reference`, `background`

Example:
```bash
--tags "nlp,transformers,foundation,must-read"
```

### Priority System

- **High**: Foundational papers, directly relevant to current work
- **Medium**: Interesting papers, useful for future reference
- **Low**: Background reading, tangentially related

### Taking Notes

Use the `--notes` field for:
- Key insights and takeaways
- Questions that arose while reading
- Connections to other papers
- Potential applications

### Rating System (1-5 stars)

- ⭐⭐⭐⭐⭐ (5): Exceptional, must-read, foundational
- ⭐⭐⭐⭐ (4): Excellent, significant contribution
- ⭐⭐⭐ (3): Good, solid work
- ⭐⭐ (2): Okay, limited impact
- ⭐ (1): Poor, not recommended

## Integration with Other Tools

### Export Reading List

The JSON files can be easily processed with other tools:

```python
import json

# Load your papers
with open('papers/to_read.json') as f:
    papers = json.load(f)

# Export to CSV, integrate with Notion, etc.
```

### Future Integration Ideas

- **BibTeX export** for citations
- **Markdown notes** with links to papers
- **Visualization** of reading progress
- **Recommendation system** based on tags
- **Collaboration features** for research groups

## Keyboard Shortcuts

For frequent use, create shell aliases:

```bash
# Add to ~/.bashrc or ~/.zshrc
alias papers='python3 /path/to/ResearchSpace/research.py papers'
alias paper-add='python3 /path/to/ResearchSpace/research.py papers add-to-read'
alias paper-read='python3 /path/to/ResearchSpace/research.py papers mark-read'
alias paper-list='python3 /path/to/ResearchSpace/research.py papers list'
alias paper-stats='python3 /path/to/ResearchSpace/research.py papers stats'
```

Then use:
```bash
paper-add "Paper Title" --authors "..." --url "..."
paper-list to-read
paper-stats
```

## Getting Help

View all available commands:

```bash
python3 research.py --help
python3 research.py papers --help
```

View help for specific command:

```bash
python3 research.py papers add-to-read --help
python3 research.py papers mark-read --help
```
