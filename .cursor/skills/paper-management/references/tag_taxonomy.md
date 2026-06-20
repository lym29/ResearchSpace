# Tag Taxonomy Guidelines

## Purpose

Consistent tagging helps organize and retrieve papers effectively. This guide provides recommended tags and usage patterns.

## Tag Categories

### 1. Research Field

Primary domain of the paper:

- `nlp` - Natural Language Processing
- `computer-vision` - Computer Vision
- `robotics` - Robotics
- `speech` - Speech Processing
- `information-retrieval` - Information Retrieval
- `recommender-systems` - Recommendation Systems
- `graph-learning` - Graph Neural Networks
- `time-series` - Time Series Analysis

### 2. Technique/Method

Specific techniques or architectures:

- `transformers` - Transformer architecture
- `attention` - Attention mechanisms
- `cnn` - Convolutional Neural Networks
- `rnn` - Recurrent Neural Networks
- `gan` - Generative Adversarial Networks
- `vae` - Variational Autoencoders
- `diffusion-models` - Diffusion Models
- `reinforcement-learning` - RL methods
- `self-supervised` - Self-supervised learning
- `few-shot` - Few-shot learning
- `zero-shot` - Zero-shot learning
- `transfer-learning` - Transfer learning
- `meta-learning` - Meta-learning

### 3. Model Type

Specific model families:

- `bert` - BERT and variants
- `gpt` - GPT models
- `t5` - T5 models
- `llm` - Large Language Models (general)
- `language-models` - Language models
- `vision-models` - Vision models
- `multimodal` - Multi-modal models
- `foundation-models` - Foundation models

### 4. Training Paradigm

How the model is trained:

- `pretraining` - Pre-training methods
- `fine-tuning` - Fine-tuning approaches
- `supervised` - Supervised learning
- `unsupervised` - Unsupervised learning
- `semi-supervised` - Semi-supervised learning
- `continual-learning` - Continual/lifelong learning
- `curriculum-learning` - Curriculum learning

### 5. Task Type

Specific tasks addressed:

- `classification` - Classification tasks
- `generation` - Generation tasks
- `translation` - Machine translation
- `summarization` - Text summarization
- `question-answering` - Q&A systems
- `dialogue` - Dialogue systems
- `image-generation` - Image generation
- `object-detection` - Object detection
- `segmentation` - Segmentation tasks

### 6. Paper Type

Nature of the paper:

- `survey` - Survey/review paper
- `tutorial` - Tutorial paper
- `benchmark` - Benchmark/dataset paper
- `analysis` - Analysis/empirical study
- `theory` - Theoretical work
- `application` - Application paper

### 7. Importance Level

Personal importance markers:

- `must-read` - Critical papers to read
- `foundation` - Foundational work in the field
- `reference` - Reference material
- `background` - Background reading
- `review-later` - To review later

### 8. Research Area

Broader research themes:

- `deep-learning` - Deep learning (general)
- `machine-learning` - Machine learning (general)
- `optimization` - Optimization methods
- `interpretability` - Model interpretability
- `efficiency` - Efficiency/compression
- `robustness` - Robustness/adversarial
- `fairness` - Fairness/ethics
- `privacy` - Privacy-preserving ML

## Tagging Best Practices

### Be Specific

✅ Good: `transformers`, `bert`, `nlp`, `pretraining`
❌ Too broad: `ai`, `ml`, `deep-learning` (as sole tags)

### Use Multiple Tags

Aim for 4-7 tags covering different categories:
- Field: `nlp`
- Technique: `transformers`, `attention`
- Model: `bert`
- Paradigm: `pretraining`
- Importance: `must-read`

### Lowercase with Hyphens

✅ Good: `reinforcement-learning`, `few-shot`
❌ Avoid: `ReinforcementLearning`, `few_shot`, `Few Shot`

### Consistency

Use the same tags for similar papers:
- Always `nlp`, not `natural-language-processing`
- Always `llm`, not `large-language-model`

## Auto-Suggested Tags

The system automatically suggests tags based on:

1. **arXiv Categories**: `cs.CL` → `cs.CL` tag
2. **Keyword Detection** in title/abstract:
   - "transformer" → `transformers`, `attention`
   - "BERT" → `bert`, `nlp`, `pretraining`
   - "vision" or "image" → `computer-vision`
   - "diffusion" → `diffusion-models`, `generative`

## When to Add Custom Tags

Add custom tags when:
- Paper relates to your specific research project
- Paper uses techniques not auto-detected
- You want to mark importance level
- Paper has specific relevance to your work

Example:
```python
add_paper_auto(
    "https://arxiv.org/abs/1706.03762",
    additional_tags=["must-read", "thesis-related", "fundamentals"]
)
```

## Tag Examples by Paper Type

### Transformer Architecture Paper
- `transformers`, `attention`, `nlp`, `deep-learning`, `foundation`

### BERT Pretraining Paper
- `bert`, `nlp`, `pretraining`, `transformers`, `language-models`, `foundation`

### GPT/LLM Paper
- `gpt`, `llm`, `language-models`, `nlp`, `generative`, `few-shot`

### Vision Transformer Paper
- `transformers`, `computer-vision`, `attention`, `image-classification`

### Survey Paper
- `survey`, `<field>`, `<topic>`, `reference`

### Diffusion Models Paper
- `diffusion-models`, `generative`, `image-generation`, `computer-vision`

### Reinforcement Learning Paper
- `reinforcement-learning`, `<environment>`, `policy-learning`

## Migration from Old Tags

If you have existing papers with different tag conventions:
1. Use `papers search` to find papers with old tags
2. Use `papers update` to standardize tags
3. Run batch updates for consistency

## Tag Analytics

Use `papers stats` to see:
- Most common tags
- Tag frequency
- Papers per tag

This helps maintain consistency and discover gaps in your reading.
