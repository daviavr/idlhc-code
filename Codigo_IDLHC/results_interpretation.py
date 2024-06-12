import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from pathlib import Path
from os import listdir
from benchmark.utils import file_name_parser
import numpy as np
import sys
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes 
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

names, colors, alphas = ["Mersenne Twister", "Mapa Logístico", "Mapa Caótico do Coseno", "Latin Hypercube Sampling"],["blue", "green", "orange", "red"], [1, 0.8, 0.6, 0.6]

def create_directories_from_str(dir_as_str):
    path = Path(dir_as_str)
    path.parent.mkdir(parents=True, exist_ok=True)

def plot_boxblot(data,num,path):
    plt.title(f'Boxplot dos valores')
    bplot = plt.boxplot(data,patch_artist=True)
    legends = []
    for patch, color, name in zip(bplot['boxes'], colors,names):
        legends.append(Patch(facecolor=color,label=name))
        patch.set_facecolor(color)
    plt.legend(handles=legends,bbox_to_anchor=(1.04, 1))
    full_path = "/home/davi/figs/" + path 
    create_directories_from_str(full_path)
    plt.savefig(full_path + "_instance_" + str(num) + "_boxplot", bbox_inches="tight")

def plot_convergence(data, num, path):
    xs,legends = [],[]
    for data_element in data:
        xs.append([i for i in range(1,len(data_element)+1)])
    
    x_min,x_max,y_min,y_max = 0,0,0,0
    do_break = False
    too_big_a_difference = False

    for element in data:
        for i in range(len(element)):
            if element[i+1] - element[i] < 0.0001 * element[i]:
                if i > x_max:
                    x_max = i
                    do_break = True
                if element[i] > y_max:
                    y_max = element[i]
                    do_break = True
                if do_break:
                    break
    x_min = x_max - 20 if x_max - 12 > 0 else 0
    x_max = x_max + 10
    y_min = y_max - (0.08 * y_max)
    y_max = y_max + (0.01 * y_max)

    biggest,smallest = max(data[0]),max(data[0])
    for i in data:
        if max(i) > biggest:
            biggest = max(i)
        if max(i) < smallest:
            smallest = max(i)

    if biggest - smallest > smallest * 0.1:
        too_big_a_difference = True 

    fig, ax = plt.subplots()
    for x,y,color,name,alpha in zip(xs,data,colors,names,alphas):
        legends.append(Patch(facecolor=color,label=name))
        ax.scatter(x,y,alpha=alpha, label=name, color=color)  

    plt.title(f'Media dos valores por geração')
    plt.ylabel("Valor da função objetivo", fontsize=10)
    plt.xlabel("Gerações", fontsize=10)
    plt.legend(handles=legends,bbox_to_anchor=(1.04, 1))

    if not too_big_a_difference:
        axins = zoomed_inset_axes(ax,2,loc="right",)  # adjust location and size as needed
        #print("limites:", x_min, x_max, y_min, y_max)
        axins.set_xlim(x_min, x_max)
        axins.set_ylim(y_min, y_max)
        plt.xticks(visible=False)
        plt.yticks(visible=False)
        for x, y, color, name, alpha in zip(xs, data, colors, names, alphas):
            axins.scatter(x, y, alpha=alpha, color=color)

        mark_inset(ax, axins, loc1=1, loc2=3, fc="none", ec="0.5")
        plt.draw()
    
    full_path = "/home/davi/figs/" + path 
    create_directories_from_str(full_path)
    plt.savefig(full_path + "_instance_" + str(num) + "_scatter", bbox_inches="tight")

def get_first_best_value(convergence_array):
    convergence_array = list(convergence_array)
    best_value = max(convergence_array)
    index_best_value = convergence_array.index(best_value)
    return best_value, index_best_value


def get_best_values_metrics(df: pd.DataFrame):
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


def get_data(current_test=0,path=""):
    folder_path = path + "/tests/"
    gen_type_path_list = listdir(Path(folder_path))

    ammount_gen_types = len(gen_type_path_list)

    averages, standard_deviations, best_values, averages_per_generation = [[0 for n in range(ammount_gen_types)] for i in range(len(names))] 
    for current_gent_type_path in gen_type_path_list:
        test_full_path = (
            folder_path
            + current_gent_type_path
            + "/"
            + path.lower()+"-instance_{current_test}.csv".format(current_test=current_test)
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

    final_best = []
    for i in best_values:
       final_best.append(max(i)) 
    #plot_boxblot(best_values,current_test,path)
    #plot_convergence(averages_per_generation,current_test,path)
    return best_values, averages, final_best, standard_deviations


def gen_full_table(path):
    final_string = "\\begin{table}\n\\centering\n\\begin{tabular}{c|c|c|c|c}\n\\hline\nPRNG & Instância & Melhor Valor & Média & Desvio Padrão \\\\ \\hline\n"
    for prng_index in range(len(names)):
        final_string = final_string + " \\multirow{9}{*}{" + names[prng_index] + "}"
        for current_test in range(9): 
            best_values, averages, final_best, standard_deviations = get_data(current_test=current_test,path=path)
            final_string = final_string + " & " + str(current_test + 1) + " & " + "\\textbf{" + str(final_best[prng_index]) + "}"  + " & " + "\\textbf{" + "{:.2f}".format(averages[prng_index]).replace('.',',') + "}" + " & " + "\\textbf{" + "{:.2f}".format(standard_deviations[prng_index]).replace('.',',') + "}" + " \\\\" + "\n"
        final_string = final_string + "\\hline"
    final_string = final_string + "\\hline\n"
    final_string = final_string + "\\end{tabular}\n"
    final_string = final_string + "\\caption{" + path + "}" + "\n"
    final_string = final_string + "\\end{table}\n\n\n"
    with open('fulltable.txt', 'w') as output:
        output.write(final_string)

def gen_per_instance_table(current_test,paths):
    final_string = ""
    for path in paths:
        final_string = final_string + "\\begin{table}\n\\centering\n"
        final_string = final_string + "\\caption{" + path + "}" + "\n"
        final_string = final_string + "\\begin{tabular}{c|c|c|c|c}\n\\hline\nPRNG & Instância & Melhor Valor & Média & Desvio Padrão \\\\ \\hline\n"
        for prng_index in range(len(names)):
            best_values, averages, final_best, standard_deviations = get_data(current_test=current_test,path=path)
            final_string = final_string + names[prng_index] + " & " + str(int(current_test) + 1) + " & " + str(final_best[prng_index]) + " & " + "{:.2f}".format(averages[prng_index]).replace('.',',') + " & " + "{:.2f}".format(standard_deviations[prng_index]).replace('.',',') + "\\\\" + "\n"
        final_string = final_string + "\\hline\n"
        final_string = final_string + "\\end{tabular}\n"
        final_string = final_string + "\\end{table}\n\n\n"
    with open('instance_table.txt', 'w') as output:
        output.write(final_string)
    

test_num = sys.argv[1]
path = sys.argv[2]


gen_full_table(path=path)
#gen_per_instance_table(current_test=test_num,paths=("MINMAX-INT","KNAPSACK-INT","U-KNAPSACK-INT"))