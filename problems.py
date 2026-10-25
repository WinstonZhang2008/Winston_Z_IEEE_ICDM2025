"""
The three microchip production problems and the three prompt strategies used in the paper.

Strategies
  copy_paste    : the problem statement as a non-expert would paste it, no guidance
  structured    : variables, objective, and constraints stated explicitly
  expert_guided : role framing, a required solving procedure, and a fixed output format

Provenance: the expert_guided LP and MILP prompts and the copy_paste NLP prompt are the
originals from the study. The remaining six variants were reconstructed after publication
from the paper's description of each strategy, so exact numbers may differ slightly from
the published tables.
"""

# ---------------------------------------------------------------- LP

LP_PROBLEM = """A company makes two types of microchips: logic chips and memory chips.
Each logic chip requires 1g silicon, 1g plastic, and 4g copper, and earns 12 euros profit.
Each memory chip requires 1g germanium, 1g plastic, and 2g copper, and earns 9 euros profit.
The company has 1000g silicon, 1500g germanium, 1750g plastic, and 4800g copper.
How many logic chips and memory chips should the company produce to maximize profit?"""

LP_STRUCTURED = """Solve the following linear programming problem.

Decision variables:
  x = number of logic chips
  y = number of memory chips

Objective: maximize profit = 12x + 9y

Constraints:
  x <= 1000         (silicon)
  y <= 1500         (germanium)
  x + y <= 1750     (plastic)
  4x + 2y <= 4800   (copper)
  x >= 0, y >= 0

Report the optimal x, optimal y, and the maximum profit."""

LP_EXPERT = """You are an expert in mathematical optimization and linear programming. Solve the following LP problem using correct calculations. Do not guess. Set up the LP, solve it using the correct mathematical method, and provide the exact optimal values and maximum profit. Your final answer must be exactly in the following format and nothing else:

Optimal x = <value>
Optimal y = <value>
Maximum profit = <value>

Problem:
A company makes two types of microchips:
Let x = number of logic chips
Let y = number of memory chips

Each logic chip requires:
1g silicon, 1g plastic, 4g copper

Each memory chip requires:
1g germanium, 1g plastic, 2g copper

The profit is:
12 euros per logic chip
9 euros per memory chip

Material constraints:
Max 1000g silicon
Max 1500g germanium
Max 1750g plastic
Max 4800g copper

Goal: Maximize profit."""

# ---------------------------------------------------------------- MILP

MILP_PROBLEM = """A company makes two types of microchips: logic chips and memory chips.
About 1% of copper is wasted during production, so each logic chip actually uses 4.04g copper
and each memory chip uses 2.02g copper. Each logic chip also requires 1g silicon and 1g plastic
and earns 12 euros; each memory chip requires 1g germanium and 1g plastic and earns 9 euros.
The company has 1000g silicon, 1500g germanium, 1750g plastic, and 4800g copper.
The company can only produce whole chips. How many of each should it produce to maximize profit?"""

MILP_STRUCTURED = """Solve the following mixed-integer linear programming problem.

Decision variables:
  x = number of logic chips (integer)
  y = number of memory chips (integer)

Objective: maximize profit = 12x + 9y

Constraints:
  x <= 1000               (silicon)
  y <= 1500               (germanium)
  x + y <= 1750           (plastic)
  4.04x + 2.02y <= 4800   (copper, including 1% waste)
  x, y >= 0 and integer

Report the optimal integer x, optimal integer y, and the maximum profit."""

MILP_EXPERT = """You are an expert in mathematical optimization and linear programming. Solve the following LP problem using correct calculations. Do not guess. Set up the LP, solve it using the correct mathematical method, and provide the exact optimal values and maximum profit. Your final answer must be exactly in the following format and nothing else:
Solve the mixed integer linear optimization problem. Return the answer in integers.
Optimal x = <value>
Optimal y = <value>
Maximum profit = <value>

Problem:
A company makes two types of microchips:
Let x = number of logic chips
Let y = number of memory chips

Each logic chip requires:
1g silicon, 1g plastic, 4.04g copper

Each memory chip requires:
1g germanium, 1g plastic, 2.02g copper

The profit is:
12 euros per logic chip
9 euros per memory chip

Material constraints:
Max 1000g silicon
Max 1500g germanium
Max 1750g plastic
Max 4800g copper

Goal: Maximize profit."""

# ---------------------------------------------------------------- NLP

NLP_PROBLEM = """A company makes two types of microchips: logic chips and memory chips.
As production increases, efficiency drops due to equipment strain, so profit per chip decays:
profit = 12 * x * exp(-0.0005 * x) + 9 * y * exp(-0.0003 * y),
where x is the number of logic chips and y is the number of memory chips.
Copper waste also scales nonlinearly: total copper used is 4.04 * x^1.02 + 2.02 * y^1.03.
Each logic chip uses 1g silicon and 1g plastic; each memory chip uses 1g germanium and 1g plastic.
The company has 1000g silicon, 1500g germanium, 1750g plastic, and 4800g copper.
How many of each chip should the company produce to maximize profit?"""

NLP_STRUCTURED = """Solve the following nonlinear programming problem.

Decision variables:
  x = number of logic chips
  y = number of memory chips

Objective: maximize profit = 12 * x * exp(-0.0005 * x) + 9 * y * exp(-0.0003 * y)

Constraints:
  x <= 1000                                (silicon)
  y <= 1500                                (germanium)
  x + y <= 1750                            (plastic)
  4.04 * x^1.02 + 2.02 * y^1.03 <= 4800    (copper)
  x >= 0, y >= 0

Use a correct numerical optimization method. Report the optimal x, optimal y, and the maximum profit."""

NLP_EXPERT = """You are an expert in mathematical optimization and nonlinear programming. Solve the following NLP problem using correct numerical methods (for example Lagrange multipliers, KKT conditions, or sequential quadratic programming). Do not guess. Your final answer must be exactly in the following format and nothing else:

Optimal x = <value>
Optimal y = <value>
Maximum profit = <value>

Problem:
Let x = number of logic chips
Let y = number of memory chips

Objective: maximize 12 * x * exp(-0.0005 * x) + 9 * y * exp(-0.0003 * y)

Constraints:
x <= 1000 (silicon)
y <= 1500 (germanium)
x + y <= 1750 (plastic)
4.04 * x^1.02 + 2.02 * y^1.03 <= 4800 (copper)
x >= 0, y >= 0"""

PROMPTS = {
    "lp":   {"copy_paste": LP_PROBLEM,   "structured": LP_STRUCTURED,   "expert_guided": LP_EXPERT},
    "milp": {"copy_paste": MILP_PROBLEM, "structured": MILP_STRUCTURED, "expert_guided": MILP_EXPERT},
    "nlp":  {"copy_paste": NLP_PROBLEM,  "structured": NLP_STRUCTURED,  "expert_guided": NLP_EXPERT},
}

# Tolerance on the reported maximum profit for an answer to count as correct.
# LP and MILP have exact optima; NLP is scored against the SLSQP optimum.
TOLERANCE = {"lp": 0.5, "milp": 0.5, "nlp": 0.01}   # absolute for lp/milp, relative for nlp
