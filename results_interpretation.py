import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from pathlib import Path
from os import listdir
from benchmark.utils import file_name_parser
import numpy as np
import sys
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes 
from mpl_toolkits.axes_grid1.inset_locator import inset_axes 
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

names, colors, alphas = ["Mersenne Twister", "Mapa Logístico", "Mapa Caótico do Coseno", "Latin Hypercube Sampling"],["red", "green", "blue", "yellow"], [1, 0.8, 0.6, 0.4]


def plot_boxblot(data):
    plt.title(f'Boxplot dos valores')
    bplot = plt.boxplot(data,labels=names,patch_artist=True)
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
    plt.show()

def plot_convergence(data):
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
    plt.legend(handles=legends,loc="lower right")

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
    
    plt.show()

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

    print(averages)
    print(standard_deviations)
    plot_boxblot(best_values)
    plot_convergence(averages_per_generation)

test_num = sys.argv[1]
path = sys.argv[2]
get_data(current_test=test_num,path=path)
