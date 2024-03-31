from common.problem import Problem
from algorithm.idlhc import IDLHC
from bench_algorithms import *
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

    folder_path = choosen_path + "/tests/population-gen-type_{population_gen_type}/".format(
        population_gen_type=population_gen_type,
    )

    file_path = choosen_path + "-instance_{instance_num}.csv".format(
        instance_num=instance_num, population_gen_type=population_gen_type
    )
    file_path = folder_path + file_path
    
    create_directories_from_str(file_path)
    
    final_test_df = save_df_to_path(path=file_path,df = pd.DataFrame(convergence_array))

    best_individual_path = "best-individuals-instance_{instance_num}/run_{run}.csv".format(
        instance_num = instance_num,
        run=final_test_df.columns[-1]
    )
    best_individual_path = folder_path + best_individual_path
    create_directories_from_str(best_individual_path)
    
    best_individual_df = pd.DataFrame()
    for individual in best_individuals:
        best_individual_df = pd.concat([best_individual_df,pd.DataFrame(individual)],axis=1,ignore_index=True)
    save_df_to_path(path=best_individual_path, df= best_individual_df,prefix="gen")
