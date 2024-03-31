import bench_algorithms as bench
def benchmark_picker(choosen_bench: str):
    if choosen_bench == "KNAPSACK":
        return bench.Knapsack
    elif choosen_bench == "U_KNAPSACK":
        return bench.UnconstrainedKnapsack
    elif choosen_bench == "MINMAX":
        return bench.MinMax
    else:
        raise Exception("Tipo não conhecido")