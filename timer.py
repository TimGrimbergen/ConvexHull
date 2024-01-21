from time import perf_counter
import numpy as np
import matplotlib.pyplot as plt

from chans_algorithm import chan
from gift_wrapping import gift_wrapping
from graham_scan import graham_scan
from create_hulls import load_hulls

def select_algorithm(alg_name):
    if alg_name == 'chan': return chan
    elif alg_name == 'gift_wrapping': return gift_wrapping
    elif alg_name == 'graham_scan': return graham_scan
    else: raise RuntimeError(f"Algorithm {alg_name} not recognized")

def timer(algorithms, folder):
    result = {alg : {} for alg in algorithms}

    test_hulls = load_hulls(folder)

    for (n,m) in test_hulls:
        for alg in algorithms:
            algorithm = select_algorithm(alg)
            result[alg][(n,m)] = [] # store generation times of each hull in a list
            for id in test_hulls[(n,m)]:
                points = [tuple(x) for x in test_hulls[(n,m)][id]['points'].tolist()]
                t_start = perf_counter()
                algorithm(points)
                t_end = perf_counter()
                result[alg][(n,m)].append(t_end - t_start)

    return result

def plot_time_results(result, algorithms, n = None, S = None):
    # expects a dictionary of (n,m) keys with generation times as values
    
    # if n or S is specified, make plot with the value for n or S fixed. So,
    # n : number of points on hull is fixed
    # S : total number of points in configuration (S = n+m) is fixed

    alg_xy = {alg : [[],[]] for alg in algorithms}

    if n:
        for alg in algorithms:
            for (nn, m) in result[alg]:
                if n == nn:
                    alg_xy[alg][0].append(n+m)
                    alg_xy[alg][1].append(np.mean(result[alg][(n,m)]))
        plt.figure()
        for alg in algorithms:
            plt.scatter(alg_xy[alg][0], alg_xy[alg][1], label=alg)
        plt.xscale('log')
        plt.yscale('log')
        plt.legend()
        plt.savefig(f"figs/timing_results/n_{n}")
    elif S:
        for alg in algorithms:
            for (nn, m) in result[alg]:
                if nn + m == S:
                    alg_xy[alg][0].append(nn)
                    alg_xy[alg][1].append(np.mean(result[alg][(nn,m)]))
        plt.figure()
        for alg in algorithms:
            plt.scatter(alg_xy[alg][0], alg_xy[alg][1], label=alg)
        plt.xscale('log')
        plt.yscale('log')
        plt.legend()
        plt.savefig(f"figs/timing_results/S_{S}")
    else:
        raise RuntimeError("Please specify either the number of points on the hull (n) or the total number of poitns (S) to get a sensible plot.")
    
if __name__ == '__main__':
    result = timer(['chan', 'graham_scan'], './hulls3')
    print(result)
    plot_time_results(result, ['chan', 'graham_scan'], n = 100)



