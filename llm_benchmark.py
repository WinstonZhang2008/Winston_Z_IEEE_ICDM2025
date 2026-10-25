"""
LLM optimization benchmark from
"Bringing Optimization to Everyone: Exploring LLMs as a Tool for Non-Experts and Students"
IEEE ICDM 2025 Undergraduate & High School Symposium.

Runs every (problem, model, prompt strategy) combination for N trials, scores each answer
against the traditional-solver optimum, and writes one row per trial to results.csv.

Usage:
    python llm_benchmark.py                      # full grid, 20 trials each
    python llm_benchmark.py --trials 5           # quick run
    python llm_benchmark.py --problems lp --models gpt-4o --strategies expert_guided
"""
import argparse
import csv
import os
import re
import time
from collections import defaultdict

from dotenv import load_dotenv
from openai import OpenAI

from problems import PROMPTS, TOLERANCE
from solvers import SOLVERS

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODELS = ["gpt-5", "gpt-4.1", "gpt-4o"]
STRATEGIES = ["copy_paste", "structured", "expert_guided"]

PROFIT_RE = re.compile(r"(?:maximum\s+profit|max\s+profit|profit)\s*[=:≈]\s*(?:€|\$)?\s*([-+]?\d[\d,]*\.?\d*)", re.I)


def extract_profit(text):
    """Pull the last reported profit figure out of a model response. Returns None if absent."""
    matches = PROFIT_RE.findall(text)
    if not matches:
        return None
    return float(matches[-1].replace(",", ""))


def is_correct(problem, reported, truth):
    if reported is None:
        return False
    tol = TOLERANCE[problem]
    if problem == "nlp":
        return abs(reported - truth) <= tol * abs(truth)
    return abs(reported - truth) <= tol


def ask(model, prompt):
    t0 = time.time()
    resp = client.responses.create(model=model, input=prompt)
    return resp.output_text, time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=20)
    ap.add_argument("--problems", nargs="+", default=list(PROMPTS), choices=list(PROMPTS))
    ap.add_argument("--models", nargs="+", default=MODELS)
    ap.add_argument("--strategies", nargs="+", default=STRATEGIES, choices=STRATEGIES)
    ap.add_argument("--out", default="results.csv")
    ap.add_argument("--verbose", action="store_true", help="print each model response")
    args = ap.parse_args()

    # Ground truth from the solvers
    truth = {}
    for p in args.problems:
        x, y, obj, _ = SOLVERS[p]()
        truth[p] = obj
        print(f"[solver] {p.upper():4} optimum: x={x:.2f} y={y:.2f} profit={obj:.2f}")

    summary = defaultdict(lambda: {"correct": 0, "n": 0, "time": 0.0})
    with open(args.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["problem", "model", "strategy", "trial", "reported_profit", "true_profit", "correct", "latency_s"])
        for p in args.problems:
            for m in args.models:
                for s in args.strategies:
                    for t in range(1, args.trials + 1):
                        text, dt = ask(m, PROMPTS[p][s])
                        reported = extract_profit(text)
                        ok = is_correct(p, reported, truth[p])
                        w.writerow([p, m, s, t, reported, round(truth[p], 2), int(ok), round(dt, 2)])
                        f.flush()
                        k = (p, m, s)
                        summary[k]["correct"] += ok
                        summary[k]["n"] += 1
                        summary[k]["time"] += dt
                        if args.verbose:
                            print(f"\n--- {p} / {m} / {s} / trial {t} ({dt:.1f}s, {'OK' if ok else 'WRONG'})\n{text}")
                        else:
                            print(f"{p:4} {m:8} {s:14} trial {t:2}  {'OK   ' if ok else 'WRONG'}  {dt:6.1f}s")

    print("\n=== Summary (accuracy %, mean latency s) ===")
    print(f"{'problem':6} {'model':9} {'strategy':14} {'acc':>6} {'time':>7}")
    for (p, m, s), v in summary.items():
        print(f"{p:6} {m:9} {s:14} {100 * v['correct'] / v['n']:5.0f}% {v['time'] / v['n']:7.2f}")
    print(f"\nPer-trial results written to {args.out}")


if __name__ == "__main__":
    main()
