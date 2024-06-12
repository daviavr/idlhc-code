from benchmark.utils import *
from benchmark.bench_algorithms import *
import sys

def run_bench_instances(bench_instance_name: str, initial_population_type: int, variables_range: list):
    tests_path = bench_instance_name + "/tests"
    bench_class, has_instances = benchmark_picker(bench_instance_name)
    
    if has_instances:        
        instances_path = bench_instance_name + "/instances/"
        benchmark_instances = listdir(Path(instances_path))
        #benchmark_instances = ["num_0|size_100.csv"]

        for current_instance in benchmark_instances:
            current_instance_info = file_name_parser(current_instance) 
            benchmark_instances_data = pd.read_csv(Path(instances_path + current_instance))

            bench_instance = bench_class(benchmark_instances_data)
            num_of_variables = current_instance_info["size"]
            
            iteration, problem, = run_test_cases(
                                    initial_population_type=initial_population_type,
                                    num_of_variables=num_of_variables,
                                    bench_instance=bench_instance,
                                    variables_range=variables_range
                                  )
            
            capture_test_data(
                iteration=iteration,
                problem=problem,
                instance_num=current_instance_info["num"],
                choosen_path=bench_instance_name
            )
    else:
        for index,current_size in enumerate(get_sizes_list()):
            iteration, problem, = run_test_cases(
                                    initial_population_type=initial_population_type,
                                    num_of_variables=current_size,
                                    bench_instance=bench_class,
                                    variables_range=variables_range
                                  )
            
            capture_test_data(
                iteration=iteration,
                problem=problem,
                instance_num=index,
                choosen_path=bench_instance_name
            )

def run_test_cases(
    initial_population_type=0,
    num_of_variables=100,
    generations=100,
    num_of_individuals=100,
    direction="MAX",
    num_pdf=20,
    num_cut_pdf=0.1,
    bench_instance = None,
    variables_range = [0,1]
):

    problem = Problem(
        num_of_variables=num_of_variables,
        num_of_individuals=num_of_individuals,
        num_of_generations=generations,
        objective=[bench_instance.bench],
        repair=[bench_instance.repair],
        mutation=(1 / num_of_variables),
        variables_range=variables_range,
        direction=direction,
        initial_population_type=initial_population_type,
    )

    iteration = IDLHC(problem, num_pdf=num_pdf, num_cut_pdf=num_cut_pdf)
    iteration.do()

    return iteration, problem
        
    
ammount_of_runs = int(sys.argv[1])
initial_population_type = int(sys.argv[2])
bench_instance_name = sys.argv[3]

variable_floor = int(sys.argv[4])
variable_ceiling = int(sys.argv[5])

for current_run in range(ammount_of_runs):
    run_bench_instances(
        bench_instance_name=bench_instance_name,
        initial_population_type=initial_population_type,
        variables_range=[variable_floor,variable_ceiling]
        )

print("done")