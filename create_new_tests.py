import random
import pandas as pd
from pathlib import Path
import math
from benchmark.bench_algorithms import *
from benchmark.utils import benchmark_picker,get_sizes_list
import sys

step_size = 100

def gen_problem_vars(num_of_variables=100, value_range=(1, 100), weight_range=(1, 100)):
    values = [random.randint(*value_range) for i in range(num_of_variables)]
    #weights = [random.randint(*weight_range) for i in range(num_of_variables)]

    return values #, weights


def save_knapsack_instances(num_of_steps, bench_instance_name):
    bench_class,has_instances = benchmark_picker(bench_instance_name)

    initial_size = bench_class.minimum_size
    
    row_df = pd.DataFrame({})
    
    for i,current_size in enumerate(get_sizes_list(initial_size=initial_size,step_size=step_size,num_steps=num_of_steps)):

        instance_values = gen_problem_vars(
            current_size,
            value_range=(bench_class.min_item_value, bench_class.max_item_value),
            #weight_range=(bench_class.min_weight_value, bench_class.max_weight_value),
        )

        #values, weights = instance_values
        values = instance_values

        problem_row = {
            "values": values,
            #"weights": weights,
        }

        instance_name = "num_{problem}|size_{size}".format(problem=i,size=current_size)
        filepath = Path(bench_instance_name + "/" +"instances/" + instance_name + ".csv")
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        row_df = pd.DataFrame(problem_row)

        row_df.to_csv(filepath, mode="w", index_label="index")


bench_instance_name = sys.argv[1]
bench_classs = benchmark_picker(bench_instance_name)

save_knapsack_instances(num_of_steps=10,bench_instance_name=bench_instance_name)