from random_convex_hull import *
from graham_scan import graham_scan
from gift_wrapping import gift_wrapping
from chans_algorithm import chan

from scipy.spatial import ConvexHull
from itertools import groupby
from tqdm import tqdm

import numpy as np

import csv
import datetime
import time
import sys


def test_method(correct_hull: ConvexHull, method=graham_scan):
    points = list(map(tuple, correct_hull.points))
    t0 = time.perf_counter_ns()
    hull = method(points)
    t1 = time.perf_counter_ns()
    correct_points = set(map(tuple, correct_hull.points[correct_hull.vertices]))
    hull_points = set(map(tuple, hull))
    return correct_points == hull_points, t1 - t0



def main():
    # Create a new file with current date and time in the name:
    now = datetime.datetime.now()
    filename = f'data/data_{now.strftime("%Y-%m-%d_%H:%M:%S")}.csv'

    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['n', 'k', 'seed', 'algorithm', 'correct', 'dt'])

        seed_gen = np.random.default_rng()

        for n, _ in groupby(np.geomspace(3, 5000, 20, dtype=int)):
            for k, _ in groupby(np.geomspace(3, n, 20, dtype=int)):
                for _ in range(250):
                    seed = seed_gen.bit_generator.random_raw()
                    rng = np.random.default_rng(seed)
                    correct_hull = random_convex_hull_with_points(k, n-k, rng=rng)
                    for method in [gift_wrapping, graham_scan, chan]:
                        name = method.__name__
                        print(f'n={n}, k={k}, seed={seed}, method={name}')
                        correct, time = test_method(correct_hull, method)
                        writer.writerow([n, k, seed, name, correct, time])

if __name__ == '__main__':
    main()
