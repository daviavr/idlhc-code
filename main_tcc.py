from common.problem import Problem
from algorithm.idlhc import IDLHC
from bench_algorithms import Knapsack
import random
import pandas as pd
from pathlib import Path


def gen_test_cases(
    generations=100,
    num_of_individuals=100,
    num_of_variables=100,
    direction="MAX",
    num_pdf=20,
    num_cut_pdf=0.1,
):
    knapsack_tests_data = pd.read_csv("test_data/knapsack.csv")
#    test = knapsack_tests_data.iloc
#    print(test[1])
    for count,data_row in enumerate(knapsack_tests_data.iloc):
        #data_row = knapsack_tests_data.iloc[0]
        capacity = int(data_row["capacity"])
        values = [int(i) for i in data_row["values"].replace("[","").replace("]", "").split(",")]
        weights = [int(i) for i in data_row["weights"].replace("[","").replace("]", "").split(",")]
        sorted_ratio_indexes = [
            int(i) for i in data_row["sorted_ratio_indexes"].replace("[","").replace("]", "").split(",")
        ]

        knapsack = Knapsack(capacity, values, weights, sorted_ratio_indexes)

        problem = Problem(
            num_of_variables=num_of_variables,
            num_of_individuals=num_of_individuals,
            num_of_generations=generations,
            objective=[knapsack.bench],
            repair=[knapsack.repair],
            mutation=(1 / num_of_variables),
            variables_range=[0, 1],
            direction=direction,
            initial_population_type=2,
        )

        iteration = IDLHC(problem, num_pdf=num_pdf, num_cut_pdf=num_cut_pdf)
        iteration.do()
        capture_test_data(iteration,problem, count)
        
def capture_test_data(iteration : IDLHC, problem: Problem, problem_number : int):
    best_value = max(iteration.convergence_array)
    convergence_array = iteration.convergence_array
    first_gen_with_best_value = 0
    population_gen_type = problem.initial_population_type
    problem_type = "knapsack"

    for count,value in enumerate(convergence_array):
        if value == best_value:
            first_gen_with_best_value = count
            break

            
    problem_row = {
    "best_value": best_value,
    "firstgen_with_best_value": first_gen_with_best_value,
    "population_gen_type": population_gen_type,
    "problem_type": problem_type,
    "convergence_array": "",
    "problem_number": problem_number 
    }

    row_df = pd.DataFrame([problem_row])
    row_df.at[0, "convergence_array"] = convergence_array

    filepath = Path("algorithm_metrics/knapsack_problem.csv")

    filepath.parent.mkdir(parents=True, exist_ok=True)

    row_df.to_csv(filepath, mode="a", index=False, header=False)


gen_test_cases()

# for i in range(len(best_values)):
# df2.at[i, "convergence_array"] = convergences[i]

# filepath = Path("metrics/knapsack.csv")



# final_dict = {}
# num_of_problems = 100
# capacity = 2000


# def gen_problem_vars():
# values = [random.randint(1, 100) for i in range(num_of_variables)]
# weights = [random.randint(1, 100) for i in range(num_of_variables)]

# ratios = [values[i] / weights[i] for i in range(num_of_variables)]

# sorted_ratio_indexes = sorted(range(len(values)), key=lambda i: ratios[i])
# return values, weights, ratios, sorted_ratio_indexes


# zero_list = ["" for i in range(num_of_problems)]

# problems_to_bench = pd.DataFrame(
# {
# "values": zero_list.copy(),
# "weights": zero_list.copy(),
# "sorted_ratio_indexes": zero_list.copy(),
# "ratios": zero_list.copy(),
# "capacity": capacity,
# }
# )


# for i in range(num_of_problems):
# values, weights, ratios, sorted_ratio_indexes = gen_problem_vars()

# problems_to_bench.at[i, "values"] = values
# problems_to_bench.at[i, "weights"] = weights
# problems_to_bench.at[i, "ratios"] = ratios
# problems_to_bench.at[i, "sorted_ratio_indexes"] = sorted_ratio_indexes


# filepath_1 = Path("problems/knapsack_problems.csv")

# filepath_1.parent.mkdir(parents=True, exist_ok=True)

# problems_to_bench.to_csv(filepath_1, mode="a", index=False, header=True)
