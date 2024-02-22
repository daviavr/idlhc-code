from os import listdir
from common.helper import file_name_parser
from pathlib import Path
import pandas as pd

population_gen_type = 0
best_individuals = [1,2,3]

instance_num = 1

folder_path = "knapsack/tests/population-gen-type_{population_gen_type}/".format(
    population_gen_type=population_gen_type,
)

file_path = "knapsack-instance_{instance_num}.csv".format(
    instance_num=instance_num, population_gen_type=population_gen_type
)
file_path = folder_path + file_path
file_path = Path(file_path)
file_path.parent.mkdir(parents=True, exist_ok=True)

row_df = pd.DataFrame()
try:
   row_df = pd.read_csv(file_path) 
   print("1")
except:
    row_df.to_csv(file_path, mode="a", index=False, header=False)
    print("2")


