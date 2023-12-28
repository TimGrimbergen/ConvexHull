from show_hull import show_hull
from random_convex_hull import random_convex_hull_with_points

import numpy as np


def left_of(a: tuple, b: tuple, c: tuple) -> bool:
    """
    Check if point c is left of the line from a to b.
    """
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) > 0


def gift_wrapping(points: list[tuple]) -> list[tuple]:
    """
    Find the convex hull of a set of points using the gift wrapping algorithm
    (aka Jarvis march).
    """
    # Find the leftmost point. If there are several leftmost points, pick the
    # one with the lowest y-coordinate.
    point_on_hull = min(points)

    hull = []
    while True:
        hull.append(point_on_hull)
        endpoint = points[0]
        for point in points[1:]:
            if endpoint == point_on_hull or left_of(hull[-1], endpoint, point):
                endpoint = point
        point_on_hull = endpoint
        if endpoint == hull[0]:
            break
    return hull

def main():
    n, m = 10, 100
    points = random_convex_hull_with_points(n, m).points.tolist()
    hull = gift_wrapping(points)
    show_hull(np.array(points), np.array(hull))


if __name__ == '__main__':
    main()