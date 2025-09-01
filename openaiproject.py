import os
from dotenv import load_dotenv
from openai import OpenAI
import time
load_dotenv()



api_key = os.getenv("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")

mathematical_optmization = """
You are an expert in mathematical optimization and linear programming. Solve the following LP problem exactly and return only three lines in this exact format (nothing else):

Optimal U = <value>
Optimal V = <value>
Maximum profit = <value>

Do not include any explanations, code, or extra text. Use correct arithmetic or a reliable solver internally; do not guess.

Problem statement:
A company produces two versions of a product. Let U = number of high-priced units produced per week. Let V = number of low-priced units produced per week.

Parameters:
U sells for 270 per unit and requires 10 grams of raw material, 1 hour of labor type A, and 2 hours of labor type B. Market demand for U is limited to 40 units per week.
V sells for 210 per unit and requires 9 grams of raw material, 1 hour of labor type A, and 1 hour of labor type B. Demand for V is unlimited.
Raw material costs 10 per gram (must be purchased and cannot be carried over; any leftover is discarded). There is effectively unlimited supply of raw material (no upper bound besides cost).
Labor A is limited to 80 hours per week and costs 50 per hour.
Labor B is limited to 100 hours per week and costs 40 per hour.

Modeling note: Treat costs for raw material and labor as part of unit costs. The objective is to maximize weekly profit (revenue minus raw material cost minus labor costs). Formulate the LP, solve it, and output only the three required lines with numeric values (use decimals if needed).
"""




linear_optimization = """
You are an expert in mathematical optimization and linear programming. Solve the following LP problem using correct calculations. Do not guess. Set up the LP, solve it using the correct mathematical method, and provide the exact optimal values and maximum profit. Your final answer must be exactly in the following format and nothing else:

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

Goal: Maximize profit.
"""


mixed_linear_optimization = """
The company BIM (Best International Machines) produces two types of microchips, logic chips (1g silicon, 1g plastic, 4g copper) and memory chips (1g germanium, 1g plastic, 2g copper). Each of the logic chips can be sold for a 12€ profit, and each of the memory chips for a 9€ profit. The current stock of raw materials is as follows: 1000g silicon, 1500g germanium, 1750g plastic, 4800g copper.

The company BIM realizes that a 1 percent fraction of the copper always gets wasted while producing both types of microchips, more specifically 1 percent of the required amount. This means that it actually takes 4.04 gr of copper to produce a logic chip and 2.02 gr of copper to produce a memory chip.

How many microchips of each type should be produced to maximize profit while respecting the availability of raw material stock? What is the maximum profit?

"""

mixed_linear_optimization2 = """
You are an expert in mathematical optimization and linear programming. Solve the following LP problem using correct calculations. Do not guess. Set up the LP, solve it using the correct mathematical method, and provide the exact optimal values and maximum profit. Your final answer must be exactly in the following format and nothing else:

Solve the mixed integer linear optimization problem. Return the answer in integers.
Optimal A = <value>
Optimal B = <value>
Optimal C = <value>
Maximum profit = <value>

Problem:
A manufacturing company produces three types of electronic devices: Device A (high-end), Device B (mid-range), and Device C (budget).

Let:
A = number of Device A produced weekly
B = number of Device B produced weekly
C = number of Device C produced weekly

Each device requires three limited resources: skilled labor, assembly time, and microchips.

Device data:
- Device A: profit €60/unit; requires 4 hours skilled labor, 3 hours assembly, 5 microchips
- Device B: profit €40/unit; requires 2 hours skilled labor, 2 hours assembly, 3 microchips
- Device C: profit €25/unit; requires 1 hour skilled labor, 1.5 hours assembly, 2 microchips

Weekly resource limits:
- Skilled labor: 500 hours
- Assembly time: 400 hours
- Microchips: 600 units

Demand limits per week:
- Device A: max 80 units
- Device B: max 150 units
- Device C: max 200 units

Contractual obligations:
- At least 30 units of Device B
- At least 50 units of Device C

Branding constraint:
- At least 20 percent of total produced units must be Device A

All decision variables must be non-negative integers.

Goal: Maximize total profit. 
Tell me the total runtime
"""

correct_x = "650"
correct_y = "1100"
correct_profit = "17700"
correct_profit2 = "17,700"

num_correct = 0
total_runs = 20

start_time = time.time()
client = OpenAI(api_key=api_key)

for i in range(20):
    response = client.responses.create(
        model="gpt-4o",
        input= """You are an expert in mathematical optimization and linear programming. Solve the following LP problem using correct calculations. Do not guess. Set up the LP, solve it using the correct mathematical method, and provide the exact optimal values and maximum profit. Your final answer must be exactly in the following format and nothing else:

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

Goal: Maximize profit.

"""
    )

    output_text = response.output_text
    print(output_text)
    print("_______________________________________")


end_time = time.time()
runtime_seconds = end_time - start_time

print(f"Runtime: {runtime_seconds:.2f} seconds")