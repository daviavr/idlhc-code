import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from pathlib import Path
from os import listdir
from common.helper import file_name_parser
import numpy as np
import sys


def plot_boxblot(data):
    names, xs = [],[]
    for gen_type, data_element in enumerate(data):
        names.append(f"Tipo de Geração {gen_type}")
        xs.append([np.random.normal(gen_type + 1, 0.04) for i in range(len(data_element))])
    
    plt.boxplot(data,labels=names)
    for x,y in zip(xs,data):
        plt.scatter(x,y,alpha=0.4)  

    #plt.axvline(avg, color='red', linestyle='dashed', linewidth=2, label='Media')
    #plt.axvline(avg + std, color='green', linestyle='dashed', linewidth=2, label=f'Media + 1 std' )
    #plt.axvline(avg - std, color='purple', linestyle='dashed', linewidth=2, label=f'Media - 1 std')

    #plt.legend()
    #axs.title(f'Dados com Media e Desvio padrão de {std:.2f}')
    #axs.xlabel('Valor')
    #axs.ylabel('Frequencia')
    plt.show()

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
        x_axis, arr1, marker="o", color="none", markeredgecolor="blue",linestyle="", markersize=3, alpha=0.5
    )
    ax.plot(
        x_axis, arr2, marker="o", color="red", linestyle="", markersize=3, alpha=0.5
    )
    ax.plot(
        x_axis, arr3, marker="s", color="green", linestyle="", markersize=3, alpha=0.5
    )
    legends = [
        Patch(facecolor="blue", label="aleatório"),
        Patch(facecolor="red", label="mapa logistico 1"),
        Patch(facecolor="green", label="mapa logistico 2"),
    ]
    ax.legend(handles=legends)
    #ax.text(13,12000,"media|media|media\ndesvio|desvio|desvio",fontsize=10)

    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    
    plt.title(f'Media dos valores por geração')
    plt.ylabel("Valor da função objetivo", fontsize=10)
    plt.xlabel("Gerações", fontsize=10)
    #plt.xlim((-0.5, 24.5))
    plt.show()
    # plt.legend()

    # plota o gráfico


def get_first_best_value(convergence_array):
    convergence_array = list(convergence_array)
    best_value = max(convergence_array)
    index_best_value = convergence_array.index(best_value)
    return best_value, index_best_value


def get_best_values_metrics(df: pd.DataFrame):
    ammount_of_rows, ammount_of_columns = df.shape
    best_values = []

    for current_column_header in df.columns:
        first_best_value, index_first_best_value = get_first_best_value(
            df[current_column_header]
        )
        # print("best_value: ", first_best_value ,"index: ",index_first_best_value)
        best_values.append(first_best_value)
    #print(best_values)

    return np.mean(best_values), np.std(best_values), best_values


def get_averages_per_generation(df: pd.DataFrame):
    averages_per_generation = []
    for row in df.iloc:
        # print("avg: ", sum(row)/len(row), "sum: ", sum(row), "len: ", len(row))
        avg = np.mean(row)
        averages_per_generation.append(avg)
    return averages_per_generation


def get_data(current_test=0):
    folder_path = "knapsack/tests/"
    gen_type_path_list = listdir(Path(folder_path))

    ammount_gen_types = len(gen_type_path_list)

    averages, standard_deviations, best_values, averages_per_generation = [[0 for n in range(ammount_gen_types)] for i in range(4)]    
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
            best_values[gen_type_num],
        ) = get_best_values_metrics(test_instance_df)
        averages_per_generation[gen_type_num] = get_averages_per_generation(
            test_instance_df
        )

    print(averages)
    print(standard_deviations)
    plot_boxblot(best_values)
    plot_convergence(averages_per_generation)

test_num = sys.argv[1]
get_data(current_test=test_num)
