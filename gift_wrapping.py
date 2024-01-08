from plot_hull import plot_hull
from random_convex_hull import random_convex_hull_with_points

import numpy as np


def left_of(a: tuple, b: tuple, c: tuple) -> bool:
    """
    Check if point c is left of the line from a to b.
    """
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) > 0


def right_of(a: tuple, b: tuple, c: tuple) -> bool:
    """
    Check if point c is right of the line from a to b.
    """
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) < 0


def dist(a: tuple, b: tuple) -> float:
    """
    Compute the squared distance between two points.
    """
    return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def gift_wrapping(points: list[tuple]) -> list[tuple]:
    """
    Find the convex hull of a set of points using the gift wrapping algorithm
    (aka Jarvis march).
    """
    point_on_hull = min(points)
    hull = []
    while True:
        hull.append(point_on_hull)
        endpoint = points[0]
        for point in points[1:]:
            if (endpoint == point_on_hull  # Endpoint is the previous point on the hull.
                    or left_of(hull[-1], endpoint, point)  # Point is left of endpoint.
                    or (not right_of(hull[-1], endpoint, point)  # Point is colinear with endpoint.
                        and dist(hull[-1], point) > dist(hull[-1], endpoint))):  # Point is further than endpoint.
                endpoint = point
        point_on_hull = endpoint
        if endpoint == hull[0]:
            break
    return hull

def main():
    n, m = 10, 100
    points = random_convex_hull_with_points(n, m).points.tolist()
    hull = gift_wrapping(points)
    plot_hull(np.array(points), np.array(hull))


if __name__ == '__main__':
    main()
