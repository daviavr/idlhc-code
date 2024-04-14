from common.problem import Problem
from algorithm.idlhc import IDLHC
import benchmark.bench_algorithms as bench
import random
import pandas as pd
from pathlib import Path
from os import listdir

def file_name_parser(file_name):
    final_dict = {}
    split_str = file_name.removesuffix(".csv").split("|")
    for str_piece in split_str:
        final_str = str_piece.split("_")
        final_dict[final_str[0]] = int(final_str[1])
    return final_dict

def benchmark_picker(choosen_bench: str):
    #return order: class type, has_test_instances
    if choosen_bench == "KNAPSACK" or choosen_bench == "KNAPSACK-INT":
        return bench.Knapsack, True
    elif choosen_bench == "U-KNAPSACK" or choosen_bench == "U-KNAPSACK-INT":
        return bench.UnconstrainedKnapsack, True
    elif choosen_bench == "MINMAX" or choosen_bench == "MINMAX-INT":
        return bench.MinMax, False
    else:
        raise Exception("Tipo não conhecido")

def get_sizes_list(initial_size=100,step_size=100,num_steps=10):
    return [(initial_size + (current_step * step_size)) for current_step in range(num_steps)]

def save_df_to_path(path,df,prefix = None):
    try:
        file = pd.read_csv(path)
    except:
        file = pd.DataFrame()
    
    final_df = pd.concat(
        [file, df], axis=1, ignore_index=True
    )
    if prefix is None:
        prefix = "run_"
    else:
        prefix = prefix + "_"
    final_df.add_prefix(prefix).to_csv(path, mode="w", index=False)
    return final_df

def create_directories_from_str(dir_as_str):
    path = Path(dir_as_str)
    path.parent.mkdir(parents=True, exist_ok=True)

def capture_test_data(iteration: IDLHC, problem: Problem, instance_num: int, choosen_path: str):
    convergence_array = iteration.convergence_array
    population_gen_type = problem.initial_population_type
    best_individuals = iteration.best_individuals

    tests_folder_path = choosen_path + "/tests/population-gen-type_{population_gen_type}/".format(
        population_gen_type=population_gen_type,
    )

    tests_file_path = choosen_path.lower() + "-instance_{instance_num}.csv".format(
        instance_num=instance_num
    )
    tests_file_path = tests_folder_path + tests_file_path
    
    create_directories_from_str(tests_file_path)

    final_test_df = save_df_to_path(path=tests_file_path,df = pd.DataFrame(convergence_array))

    best_individuals_path = "best-individuals-instance_{instance_num}/run_{run}.csv".format(
        instance_num = instance_num,
        run=final_test_df.columns[-1]
    )
    best_individuals_path = tests_folder_path + best_individuals_path
    create_directories_from_str(best_individuals_path)
    
    best_individuals_df = pd.DataFrame()
    for individual in best_individuals:
        best_individuals_df = pd.concat([best_individuals_df,pd.DataFrame(individual)],axis=1,ignore_index=True)

    save_df_to_path(path=best_individuals_path, df= best_individuals_df,prefix="gen")
