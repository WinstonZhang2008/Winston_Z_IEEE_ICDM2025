import os
from dotenv import load_dotenv
from openai import OpenAI
import time
load_dotenv()



api_key = os.getenv("your own api key")

nonlinear_optimization = """
A company sells a product where the price decreases as more units are sold, following the demand curve:
p(x) = 100 - 2x, where p is the price per unit and x is the quantity sold.  
The total cost to produce x units is given by:
c(x) = 5x + 0.1x².  

The profit function is:
π(x) = p(x)*x - c(x).

Constraints:
1. The production quantity must be nonnegative: x ≥ 0.  
2. Due to factory capacity, production cannot exceed 40 units: x ≤ 40.  
3. To satisfy minimum customer demand, production must be at least 5 units: x ≥ 5.  
4. Since fractional units cannot be produced, x must be an integer.  

Objective:
Maximize profit π(x).

Output format:
Optimal production quantity x = <value>, Maximum profit = <value>.

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
You are an expert in mathematical optimization and linear programming. Solve the following LP problem using correct calculations. Do not guess. Set up the LP, solve it using the correct mathematical method, and provide the exact optimal values and maximum profit. Your final answer must be exactly in the following format and nothing else:
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

Goal: Maximize profit.

"""




num_correct = 0
total_runs = 20

start_time = time.time()
client = OpenAI(api_key=api_key)


#Run it 20 times
for i in range(20):
    response = client.responses.create(
        model="gpt-4o",
        input= linear_optimization

    )

    #outputs the response, used to analyze their reasoning patterns
    output_text = response.output_text
    print(output_text)
    print("_______________________________________")


end_time = time.time()
runtime_seconds = end_time - start_time

#Divide runtime by 20 to get average time
print(f"Runtime: {runtime_seconds:.2f} seconds")
