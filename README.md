# Bringing Optimization to Everyone: LLMs as a Tool for Non-Experts and Students

Code and results for the paper published at the **IEEE ICDM 2025 Undergraduate & High School Symposium** (ICDMW proceedings).

📄 [Paper on IEEE Xplore](https://ieeexplore.ieee.org/document/11415807)

## What this tests

Can a non-expert solve an optimization problem by typing it into ChatGPT in plain English? We evaluated **GPT-5, GPT-4.1, and GPT-4o** on three problem types (linear, mixed-integer, and nonlinear programming) across **three prompt strategies**, 20 trials per combination, 180 runs total, measuring accuracy and latency against traditional solvers.

## The problems

All three are versions of one microchip production problem (from the [MO-book](https://mobook.github.io/MO-book/) BIM example), so the only thing that changes between them is the type of optimization.

| Problem | What changes | Solver baseline |
|---|---|---|
| **LP** | Linear profit, linear material constraints | OR-Tools GLOP |
| **MILP** | 1% copper waste (4.04g / 2.02g per chip), whole chips only | OR-Tools CP-SAT |
| **NLP** | Profit decays with volume, copper use scales nonlinearly | SciPy SLSQP |

## Prompt strategies

| Strategy | Description |
|---|---|
| **Copy-Paste** | The problem statement pasted as written, no guidance |
| **Structured** | Variables, objective, and constraints stated explicitly |
| **Expert-Guided** | Role framing ("you are an expert in mathematical optimization"), a required solving procedure, and a fixed output format |

## Results (from the paper)

Accuracy over 20 trials, best and worst prompt strategy per cell:

| Problem | GPT-5 | GPT-4.1 | GPT-4o |
|---|---|---|---|
| LP | 100% (all prompts) | 80 to 100% | 35 to 45% |
| MILP | 100% (all prompts) | 35 to 65% | 15 to 25% |
| NLP | 55 to 100% | 25 to 100% | 20 to 35% |

Solvers: 100% accuracy on every problem, under 0.1 seconds, 100 to 1,000x faster than the fastest LLM.

**Main findings:** prompt structure matters more than model size on NLP, where Structured prompts took GPT-5 from 55% to 100% and GPT-4.1 from 25% to 100%. Mid-tier models cannot reliably enforce integrality on MILP regardless of prompting. Solvers remain the right tool for correctness; LLMs offer interpretability and a path into optimization for people without a math background.

## Repository

```
problems.py        the three problems x three prompt strategies, and scoring tolerances
solvers.py         GLOP / CP-SAT / SLSQP baselines; ground truth for scoring
llm_benchmark.py   runs the full grid against the OpenAI API, writes results.csv
```

## Running it

```bash
pip install -r requirements.txt
cp .env.example .env        # add your OpenAI API key

python solvers.py           # solver baselines only, no API key needed
python llm_benchmark.py     # full 180-trial grid (takes a while; costs API credits)

# smaller runs
python llm_benchmark.py --trials 5
python llm_benchmark.py --problems lp milp --models gpt-4o --strategies expert_guided --verbose
```

Each trial's reported profit, correctness, and latency go to `results.csv`. An answer is correct when its reported maximum profit matches the solver optimum (within 0.5 for LP and MILP, within 1% for NLP).

## A note on provenance

The original study was run with a single script that held one problem at a time. This repository restructures that code so the whole grid runs from one command. The Expert-Guided prompts for LP and MILP and the Copy-Paste prompt for NLP are the originals from the study; the other six prompt variants were reconstructed from the paper's description of each strategy. Exact accuracy numbers may therefore differ slightly from the published tables, and model outputs are nondeterministic between runs.

## Authors

Winston Zhang and Mia Lu, advised by Prof. Haibing Lu (Santa Clara University).
