# Bringing Optimization to Everyone: LLMs as a Tool for Non-Experts and Students

Code and results for the paper published at the **IEEE ICDM 2025 Undergraduate & High School Symposium** (ICDMW proceedings).
📄 [Paper on IEEE Xplore](https://ieeexplore.ieee.org/document/11415807)

## What this tests

Can a non-expert solve an optimization problem by typing it into ChatGPT in plain English? We evaluated **GPT-5, GPT-4.1, and GPT-4o** on three problem types (linear, mixed-integer, and nonlinear programming) across **three prompt strategies** and 20 trials per combination, 180+ runs total, measuring accuracy and latency against traditional solvers.

## Prompt strategies

| Strategy | Description |
|---|---|
| Copy-Paste | The problem statement pasted verbatim, as a non-expert would |
| Structured | Variables, objective, and constraints stated explicitly |
| Expert-Guided | Role framing plus a step-by-step solving procedure and a fixed output format |

## Results

| Problem | GPT-5 | GPT-4.1 | GPT-4o |
|---|---|---|---|
| LP | 100% (all prompts) | 80 to 100% | 35 to 45% |
| MILP | 100% (all prompts) | 35 to 65% | 15 to 25% |
| NLP | 55 to 100% | 25 to 100% | 20 to 35% |

Baselines: OR-Tools GLOP (LP), CP-SAT (MILP), and SciPy (NLP) each solved every problem correctly in under 0.1 seconds, 100 to 1,000x faster than the fastest LLM.

**Main findings:** prompt structure matters more than model size on NLP, where structured prompts took GPT-5 from 55% to 100%; mid-tier models cannot reliably enforce integrality on MILP regardless of prompting; and solvers remain the right tool for correctness, while LLMs offer interpretability and accessibility.

## Running it

```bash
pip install openai python-dotenv
cp .env.example .env     # add your OpenAI API key
python openaiproject.py
```

The script runs one problem 20 times, prints each trial's reasoning, and reports total and average latency.
