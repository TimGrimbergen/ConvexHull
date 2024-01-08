"""
Chan's algorithm for convex hulls based on:
https://www.cs.umd.edu/~patras/patra2012_convexhull_report.pdf
"""
from graham_scan import graham_scan
from random_convex_hull import random_convex_hull
from plot_hull import plot_hull

import numpy as np
import matplotlib.pyplot as plt


LEFT_TURN = 1
RIGHT_TURN = -1
COLINEAR = 0


def orientation(a: tuple, b: tuple, c: tuple) -> bool:
    """
    Computes the orientation of the line a-c relative to the line a-b.
    Returns 1 if a-c is a left turn from a-b, -1 if a-c is a right turn from
    a-b, and 0 if a-c is colinear with a-b.
    """
    val = (b[1] - a[1]) * (c[0] - b[0]) - (b[0] - a[0]) * (c[1] - b[1])
    if val > 0:
        return LEFT_TURN
    elif val < 0:
        return RIGHT_TURN
    else:
        return COLINEAR


def dist(a: tuple, b: tuple) -> float:
    """
    Compute the squared distance between two points.
    """
    return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def left_tangent(point: tuple, hull: list[tuple]) -> tuple:
    """
    Find the left tangent of a point and a convex hull.
    Based on:
    https://github.com/ypranay/Convex-Hull/blob/master/ChansAlgorithmForConvexHull.cpp
    line 95-115
    """
    n = len(hull)
    l, r = 0, n
    while l < r:
        c = (l + r) // 2
        c_side = orientation(point, hull[l], hull[c])
        c_prev = orientation(point, hull[c], hull[(c - 1) % n])
        c_next = orientation(point, hull[c], hull[(c + 1) % n])
        l_prev = orientation(point, hull[l], hull[(l - 1) % n])
        l_next = orientation(point, hull[l], hull[(l + 1) % n])
        if c_prev != RIGHT_TURN and c_next != RIGHT_TURN:
            return hull[c]
        elif c_side == LEFT_TURN and (l_next == RIGHT_TURN or l_prev == l_next) \
                or c_side == RIGHT_TURN and c_prev == RIGHT_TURN:
            r = c
        else:
            l = c + 1
    return hull[l]



def partial_hull(points: list[tuple], m: int) -> list[tuple]:
    """
    Find the convex hull of a set of points using the partial hull algorithm.
    """
    # Split points into m subsets.
    subsets = [points[i::m] for i in range(m)]
    # Find the convex hull of each subset.
    hulls = [graham_scan(subset) for subset in subsets]
    # Merge the convex hulls.
    p0 = min(points)
    hull = [p0]


def main():
    n = 10
    hull = random_convex_hull(n).points.tolist()
    point = (0, 1)
    plt.plot(*np.array([point, left_tangent(point, hull)]).T, 'r-o')
    plot_hull(np.array(hull), np.array(hull))
    plt.show()


if __name__ == '__main__':
    main()
