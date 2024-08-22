# tech_radar
Simplest Tech Radar creator in python

## Install

```bash
poetry shell
poetry install
```

## Use

Define a yaml like:

```yaml
---
quadrants:
  - LLM / GenAI
  - Analysis Tools
  - Programming Languages
  - IaC

categories:
  - Adopt
  - Trial
  - Assess
  - Hold

technologies:
  LLM / GenAI:
    Adopt:
    Trial:
    Assess:
      - chag-gpt
      - claude
    Hold:
      - code-llama
      - monocle
```

Then run

```bash
tech-radar --input-yaml example.yml --output example.svg
```

![Generated image](example.svg)

## Yaml details:

### Title

Optional.

Two options:

```yaml
title: My Title
```

```yaml
title:
  caption: My Title
  color: red
  fontsize: 16
```

### Quadrants

Just the list of quadrants. 2 or more.

```yaml
quadrants:
  - LLM / GenAI
  - Analysis Tools
  - Programming Languages
  - IaC
```

### Categories

The categories are the circles. In a tech radar, the usual categories are:

```yaml
categories:
  - Adopt
  - Trial
  - Assess
  - Hold
```

### Technologies

A combination of quadrants/categories/technologies:

```yaml
  Analysis Tools:
    Adopt:
      - tool1
      - tool2
    Trial:
      - tool3: outgoing
    Assess:
      - tool4: incoming
      - tool5
    Hold:
      - tool6
      - tool7
```

The quadrants and categories have to match those specified before.

Additionally, technologies can be annotated as 'incoming' or 'outgoing', changing the symbol.