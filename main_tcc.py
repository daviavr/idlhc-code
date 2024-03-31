from benchmark.utils import *
from benchmark.bench_algorithms import *
from benchmark.problems import benchmark_picker
import sys

def gen_test_cases(
    initial_population_type=0,
    generations=100,
    num_of_individuals=100,
    direction="MAX",
    num_pdf=20,
    num_cut_pdf=0.1,
    bench_instance = None
):
    instances_path = choosen_path + "/instances/"
    tests_path = choosen_path + "/tests"
    benchmark_instances = listdir(Path(instances_path))
    #benchmark_instances = ["num_0|size_100.csv"]

    for current_instance in benchmark_instances:
        benchmark_instances_data = pd.read_csv(Path(instances_path + current_instance))

        current_instance_info = file_name_parser(current_instance)

        values = list(benchmark_instances_data["values"])
        weights = list(benchmark_instances_data["weights"])

        knapsack = UnconstrainedKnapsack(values, weights)

        num_of_variables = current_instance_info["size"]

        problem = Problem(
            num_of_variables=num_of_variables,
            num_of_individuals=num_of_individuals,
            num_of_generations=generations,
            objective=[lambda individual : sum(individual.features)],
            repair=[lambda a : None],
            mutation=(1 / num_of_variables),
            variables_range=[0, 1],
            direction=direction,
            initial_population_type=initial_population_type,
        )

        iteration = IDLHC(problem, num_pdf=num_pdf, num_cut_pdf=num_cut_pdf)
        iteration.do()
        
        capture_test_data(
            iteration=iteration,
            problem=problem,
            instance_num=current_instance_info["num"],
            choosen_path=choosen_path)

num_runs = int(sys.argv[1])
gen_type = int(sys.argv[2])
choosen_path = sys.argv[3]

bench_instance = benchmark_picker(choosen_path)

for i in range(num_runs):
    gen_test_cases(
     bench_instance=bench_instance,
     initial_population_type=gen_type,
     choosen_path=choosen_path)

print("done")
