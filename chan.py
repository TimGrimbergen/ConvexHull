"""
Chan's algorithm for convex hulls based on:
https://www.cs.umd.edu/~patras/patra2012_convexhull_report.pdf
"""
from graham_scan import graham_scan
from random_convex_hull import random_convex_hull, random_convex_hull_with_points
from plot_hull import plot_hull

import itertools as it
import numpy as np
import matplotlib.pyplot as plt


LEFT = 1
RIGHT = -1
COLINEAR = 0


def orientation(a: tuple, b: tuple, c: tuple) -> bool:
    """
    Computes wether c is to the left or right of or colinear with the line ab.
    """
    val = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
    if val > 0:
        return LEFT
    elif val < 0:
        return RIGHT
    else:
        return COLINEAR


def left_tangent(point: tuple, hull: list[tuple]) -> tuple:
    """
    Find the left tangent of a point and a convex hull.
    Based on:
    https://github.com/ypranay/Convex-Hull/blob/master/ChansAlgorithmForConvexHull.cpp
    line 95-115
    """
    n = len(hull)
    left, right = 0, n - 1
    while left < right:
        center = (left + right) // 2
        left_center = orientation(point, hull[left], hull[center])
        left_next   = orientation(point, hull[left], hull[(left + 1) % n])
        left_prev   = orientation(point, hull[left], hull[(left - 1) % n])
        center_prev = orientation(point, hull[center], hull[(center - 1) % n])
        center_next = orientation(point, hull[center], hull[(center + 1) % n])
        if center_prev != LEFT and center_next == RIGHT:
            return hull[center]
        elif left_prev != LEFT and center_next == RIGHT \
                or left_prev != LEFT and left_center == RIGHT \
            right = center
        else:
            left = center + 1
    return hull[left % n]



def partial_hull(points: list[tuple], m: int) -> list[tuple] | None:
    """
    Find the convex hull of a set of points using the partial hull algorithm.
    """
    plt.plot(*np.array(points).T, 'o')
    # Split points into ceil(n/m) subsets.
    n_div_m = (len(points) + m - 1) // m
    subsets = [points[i::n_div_m] for i in range(n_div_m)]
    # Find the convex hull of each subset using graham scan.
    subhulls = [graham_scan(subset) for subset in subsets]
    for subhull in subhulls:
        plt.plot(*np.array(subhull + subhull[:1]).T, 'o-')
    # Merge the convex hulls.
    p0 = min(points)
    hull = [p0]
    for _ in range(m):
        # Compute the left tangent from the last point in the hull to each subhull.
        tangents = [left_tangent(hull[-1], subhull) for subhull in subhulls]
        # Find the leftmost tangent.
        leftmost_tangent = tangents[0]
        for tangent in tangents[1:]:
            if orientation(hull[-1], leftmost_tangent, tangent) == LEFT:
                leftmost_tangent = tangent
        if leftmost_tangent == p0:
            return hull
        hull.append(leftmost_tangent)
    plt.plot(*np.array(hull + hull[:1]).T, 'o-k')
    plt.show()
    return None


def chan(points: list[tuple]) -> list[tuple]:
    """
    Find the convex hull of a set of points using Chan's algorithm.
    """
    for t in it.count():
        m = 2 ** (2 ** t)
        hull = partial_hull(points, m)
        if hull is not None:
            return hull


def main():
    n, m = 16, 64
    points = np.flip(random_convex_hull(n).points, axis=0).tolist()
    # hull = chan(points)
    # plot_hull(np.array(points), np.array(hull))
    # plt.show()
    # vs =[(0, 0), (1, 0), (1, 1)]
    # print(orientation(*vs))

    for i in range(len(points)):
        plt.plot(*np.array(points[i - 1:i + 1]).T, 'o-')
        point = points[i]
        tangent = left_tangent(point, points)
        plt.plot(*np.array(points + points[:1]).T, 'o-')
        plt.plot(*np.array([point, tangent]).T, 'o-')
        plt.annotate(f'p', point)
        plt.annotate(f't', tangent)
        plt.show()


if __name__ == '__main__':
    main()
