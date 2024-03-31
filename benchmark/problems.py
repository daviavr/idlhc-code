import benchmark.bench_algorithms as bench
def benchmark_picker(choosen_bench: str):
    if choosen_bench == "KNAPSACK":
        return bench.Knapsack, True
    elif choosen_bench == "U_KNAPSACK":
        return bench.UnconstrainedKnapsack, True
    elif choosen_bench == "MINMAX":
        return bench.MinMax, False
    else:
        raise Exception("Tipo não conhecido")