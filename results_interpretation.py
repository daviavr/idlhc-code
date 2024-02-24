import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from pathlib import Path
from os import listdir
from common.helper import file_name_parser
import numpy as np


def plot_convergence(elements):
    arr1 = elements[0]
    arr2 = elements[1]
    arr3 = elements[2]

    # cria a figura
    # plt.style.use("seaborn-white")
    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

    # define o eixo x
    x_axis = [i for i in range(len(arr1))]

    ax.plot(
        x_axis, arr1, marker="o", color="blue", linestyle="", markersize=3, alpha=0.5
    )
    ax.plot(
        x_axis, arr2, marker="o", color="red", linestyle="", markersize=3, alpha=0.5
    )
    ax.plot(
        x_axis, arr3, marker="o", color="green", linestyle="", markersize=3, alpha=0.5
    )
    legends = [
        Patch(facecolor="blue", label="pGenType_0"),
        Patch(facecolor="red", label="pGenType_1"),
        Patch(facecolor="green", label="pGenType_2"),
    ]
    ax.legend(handles=legends)
    ax.text(13,12000,"media|media|media\ndesvio|desvio|desvio",fontsize=10)

    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.ylabel("Valor da função objetivo", fontsize=10)
    plt.xlabel("Gerações", fontsize=10)
    plt.xlim((-0.5, 20.5))
    # plt.legend()

    # plota o gráfico
    plt.show()


def get_first_best_value(convergence_array):
    convergence_array = list(convergence_array)
    best_value = max(convergence_array)
    index_best_value = convergence_array.index(best_value)
    return best_value, index_best_value


def get_best_values_metrics(df: pd.DataFrame):
    ammount_of_rows, ammount_of_columns = df.shape
    total_sum = 0
    best_values = []

    for current_column_header in df.columns:
        first_best_value, index_first_best_value = get_first_best_value(
            df[current_column_header]
        )
        # print("best_value: ", first_best_value ,"index: ",index_first_best_value)
        best_values.append(first_best_value)
        total_sum += first_best_value
    #print(best_values)

    return total_sum / ammount_of_columns, np.std(best_values)


def get_averages_per_generation(df: pd.DataFrame):
    averages_per_generation = []
    for row in df.iloc:
        # print("avg: ", sum(row)/len(row), "sum: ", sum(row), "len: ", len(row))
        avg = sum(row) / len(row)
        averages_per_generation.append(avg)
    return averages_per_generation


def get_data(current_test=0):
    folder_path = "knapsack/tests/"
    gen_type_path_list = listdir(Path(folder_path))

    averages = [0, 0, 0]
    standard_deviations = [0, 0, 0]
    averages_per_generation = [0, 0, 0]

    for current_gent_type_path in gen_type_path_list:
        test_full_path = (
            folder_path
            + current_gent_type_path
            + "/"
            + "knapsack-instance_{current_test}.csv".format(current_test=current_test)
        )
        test_full_path = Path(test_full_path)
        current_gen_data = file_name_parser(current_gent_type_path)
        test_instance_df = pd.read_csv(test_full_path)
        gen_type_num = current_gen_data["population-gen-type"]

        (
            averages[gen_type_num],
            standard_deviations[gen_type_num],
        ) = get_best_values_metrics(test_instance_df)
        averages_per_generation[gen_type_num] = get_averages_per_generation(
            test_instance_df
        )

    print(averages)
    print(standard_deviations)
    plot_convergence(averages_per_generation)


get_data(current_test=9)
