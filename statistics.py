import constants as const
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
def parametr_statistics(bacteries, parametr, matrix, era):
    matrix.append([])
    #time_line = (era-1)*const.era_period
    for bac in bacteries:
        matrix[:][era].append(getattr(bac, parametr))
    print(matrix)
    mean = np.mean(matrix[era][1:])
    if len(bacteries) > 1:
        deviation = np.std(matrix[era][1:])
    else:
        deviation = 0
    return mean, deviation


def collect_statistics(bacteries, matrix1, matrix2, matrix3, matrix_stat, era):
    mean_speed, deviation_speed = parametr_statistics(bacteries, const.parametrs[0], matrix1, era)
    mean_sens, deviation_sens = parametr_statistics(bacteries, const.parametrs[1], matrix2, era)
    mean_size, deviation_size = parametr_statistics(bacteries, const.parametrs[2], matrix3, era)

    num_bac = len(bacteries)
    row = {'time, tick': era * const.era_period, 'N bacteries': num_bac, 'mean speed': mean_speed, 'deviation speed': deviation_speed,
           'mean sens': mean_sens, 'deviation sens': deviation_sens, 'mean size': mean_size, 'deviation size': deviation_size}
    matrix_stat.loc[era] = row
    # matrix_stat.append([])
    # matrix_stat[:][era].append((era-1) * const.era_period)
    # matrix_stat[:][era].append(num_bac)
    # matrix_stat[:][era].append(mean_speed)
    # matrix_stat[:][era].append(deviation_speed)
    # matrix_stat[:][era].append(mean_sens)
    # matrix_stat[:][era].append(deviation_sens)
    # matrix_stat[:][era].append(mean_size)
    # matrix_stat[:][era].append(deviation_size)


def hist_stat(N_figure, matrix, parametr, era1, era2, interactive = True): # для отображения сравнительной гистограммы
    plt.figure(N_figure)
    plt.style.use('seaborn-deep')
    min_val = math.floor(min(matrix[era1] + matrix[era2]) / 10) * 10
    max_val = math.ceil(max(matrix[era1] + matrix[era2]) / 10) * 10
    N_bins = 20 # число столбиков в столбчатой диаграмме
    bins = np.linspace(min_val, max_val, N_bins)
    plt.hist(matrix[era1][1:], bins, alpha=0.5, density = True, label='time = %d, tick' %(int((era1-1) * const.era_period)))
    plt.hist(matrix[era2][1:], bins, alpha=0.5, density = True, label='time = %d, tick' %(int((era2-1) * const.era_period)))

    #plt.hist([matrix[era1][1:], matrix[era2][1:]], bins, label=['time = %d, tick' %(int(era1 * const.era_period)),
                                                                #'time = %d, tick' %(int(era2 * const.era_period))])
    plt.title(parametr + ' at start and end time')
    plt.legend(loc='upper right')
    plt.interactive(interactive)
    plt.show()

def plot_line(N_figure, x, y, interactive = True):
    plt.figure(N_figure)
    plt.plot(x, y, "o-", alpha=0.4)
    plt.title('Number of bacteries in different times')
    plt.interactive(interactive)
    plt.show()

def boxplot(N_figure, matrix, time_line, parametr, interactive = True):
    plt.figure(N_figure)
    # df2 = pd.DataFrame(matrix[1:])
    # df2 = pd.DataFrame.transpose(df2)
    # df2 = df2.dropna()
    # print(df2)
    plt.boxplot(matrix[1:])
    plt.title(parametr + ' in different times')
    plt.interactive(interactive)
    plt.show()