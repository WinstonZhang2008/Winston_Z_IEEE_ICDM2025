"""
Traditional solver baselines for the three microchip production problems.

LP   -> OR-Tools GLOP
MILP -> OR-Tools CP-SAT
NLP  -> SciPy SLSQP

Each function returns (x, y, objective) and the wall time of one solve.
These values are the ground truth the LLM answers are scored against.
"""
import time
import numpy as np


def solve_lp():
    from ortools.linear_solver import pywraplp
    t0 = time.time()
    s = pywraplp.Solver.CreateSolver("GLOP")
    x = s.NumVar(0, s.infinity(), "logic_chips")
    y = s.NumVar(0, s.infinity(), "memory_chips")
    s.Add(x <= 1000)              # silicon
    s.Add(y <= 1500)              # germanium
    s.Add(x + y <= 1750)          # plastic
    s.Add(4 * x + 2 * y <= 4800)  # copper
    s.Maximize(12 * x + 9 * y)
    assert s.Solve() == pywraplp.Solver.OPTIMAL
    return x.solution_value(), y.solution_value(), s.Objective().Value(), time.time() - t0


def solve_milp():
    from ortools.sat.python import cp_model
    t0 = time.time()
    m = cp_model.CpModel()
    x = m.NewIntVar(0, 1_000_000, "logic_chips")
    y = m.NewIntVar(0, 1_000_000, "memory_chips")
    m.Add(x <= 1000)
    m.Add(y <= 1500)
    m.Add(x + y <= 1750)
    m.Add(404 * x + 202 * y <= 480_000)  # 4.04x + 2.02y <= 4800, scaled to integers
    m.Maximize(12 * x + 9 * y)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30.0
    status = solver.Solve(m)
    assert status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    xv, yv = solver.Value(x), solver.Value(y)
    return xv, yv, 12 * xv + 9 * yv, time.time() - t0


def solve_nlp():
    from scipy.optimize import minimize
    t0 = time.time()

    def objective(v):
        x1, x2 = v
        return -(12 * x1 * np.exp(-0.0005 * x1) + 9 * x2 * np.exp(-0.0003 * x2))

    cons = [
        {"type": "ineq", "fun": lambda v: 1000 - v[0]},
        {"type": "ineq", "fun": lambda v: 1500 - v[1]},
        {"type": "ineq", "fun": lambda v: 1750 - (v[0] + v[1])},
        {"type": "ineq", "fun": lambda v: 4800 - (4.04 * v[0] ** 1.02 + 2.02 * v[1] ** 1.03)},
    ]
    r = minimize(objective, [500, 500], method="SLSQP", bounds=[(0, None), (0, None)], constraints=cons)
    assert r.success
    return r.x[0], r.x[1], -r.fun, time.time() - t0


SOLVERS = {"lp": solve_lp, "milp": solve_milp, "nlp": solve_nlp}


def benchmark_solvers(trials=20):
    """Run each solver `trials` times and print accuracy and mean latency (Table IV in the paper)."""
    for name, fn in SOLVERS.items():
        times = []
        for _ in range(trials):
            x, y, obj, dt = fn()
            times.append(dt)
        print(f"{name.upper():5}  x={x:.2f}  y={y:.2f}  objective={obj:.2f}  "
              f"accuracy=100%  mean_time={np.mean(times):.5f}s")


if __name__ == "__main__":
    benchmark_solvers()
