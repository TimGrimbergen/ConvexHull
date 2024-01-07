import time
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
            result[alg][(n,m)] = [] # store generation times of each hull in a list
            for id in test_hulls[(n,m)]:
                points = [tuple(x) for x in test_hulls[(n,m)][id]['points'].tolist()]
                algorithm = select_algorithm(alg)
                t_start = time.time()
                algorithm(points)
                t_end = time.time()
                result[alg][(n,m)].append(t_end-t_start)

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
        plt.legend()
        plt.show()
    elif S:
        n_vals = []
        time_vals = []
        for (n, m) in result:
            if n + m == S:
                n_vals.append(n)
                time_vals.append(np.mean(result[(n,m)]))
        plt.figure()
        plt.plot(n_vals, time_vals)
        plt.show()
    else:
        raise RuntimeError("Please specify either the number of points on the hull (n) or the total number of poitns (S) to get a sensible plot.")
    
if __name__ == '__main__':
    result = timer(['chan', 'graham_scan', 'gift_wrapping'], './hulls')
    print(result)
    plot_time_results(result, ['chan', 'graham_scan', 'gift_wrapping'], n=20)



