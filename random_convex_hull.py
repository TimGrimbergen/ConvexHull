import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull, Delaunay


def random_convex_hull(n: int, rng=None) -> ConvexHull:
    """
    Generate random convex hull with n points on the hull.
    """
    assert n >= 3, 'n must be greater than or equal to 3'
    rng = np.random.default_rng() if rng is None else rng

    # Generate 2 sets of sorted random points
    x, y = np.sort(rng.random((2, n)), axis=1)

    # Create masks to split each set into 2 subsets, keeping the first and last
    # in both subsets.
    mx1, mx2, my1, my2 = np.ones((4, n), dtype=bool)
    mx1[1:-1] = rng.integers(0, 2, size=n-2, dtype=bool)
    mx2[1:-1] = ~mx1[1:-1]
    my1[1:-1] = rng.integers(0, 2, size=n-2, dtype=bool)
    my2[1:-1] = ~my1[1:-1]

    # Compute the differences between the points in subset 1 from front to back
    # and subset 2 from back to front and concatenate them.
    x = np.concatenate((np.diff(x[mx1]), np.diff(np.flip(x[mx2]))))
    y = np.concatenate((np.diff(y[my1]), np.diff(np.flip(y[my2]))))

    # Randomly pair x and y into vectors.
    xy = np.array([rng.permutation(x), rng.permutation(y)]).T

    # Sort the vectors by angle.
    xy = xy[np.argsort(np.arctan2(xy[:, 1], xy[:, 0]))]

    # Compute vertices from the vectors.
    xy = np.cumsum(xy, axis=0)

    # Center the vertices on [0.5, 0.5]. This is not strictly necessary but
    # ensures that no points are outside the unit square.
    xy -= (xy.max(axis=0) + xy.min(axis=0) - 1) / 2

    # Return the convex hull.
    return ConvexHull(xy)


def random_points_in_delaunay(tri: Delaunay, n: int, rng=None) -> np.ndarray:
    """Generate n random points in the convex hull."""
    assert n >= 0, 'n must be greater than or equal to 0'
    rng = np.random.default_rng() if rng is None else rng

    # Compute the area of each triangle in the delaunay triangulation.
    area = tri_area_2d(tri.points[tri.simplices])

    # randomly select a triangle weighted by the area.
    tri_idx = rng.choice(len(area), size=n, p=area/area.sum())

    # Generate random points in the selected triangles using Kraemer's method.
    a = tri.points[tri.simplices[tri_idx, 0]]
    b = tri.points[tri.simplices[tri_idx, 1]]
    c = tri.points[tri.simplices[tri_idx, 2]]
    x, y = rng.random((2, n))
    q = np.abs(x - y)
    s, t, u = q, (x + y - q) / 2, 1 - (x + y + q) / 2
    return a * s[:, None] + b * t[:, None] + c * u[:, None]


def tri_normal_2d(tris: np.ndarray) -> np.ndarray:
    """Compute the normal vectors of a list of triangles."""
    return np.cross(tris[:, 1] - tris[:, 0],
                    tris[:, 2] - tris[:, 0], axis=1)


def tri_area_2d(tris: np.ndarray) -> np.ndarray:
    """Compute the area of a list of triangles."""
    return tri_normal_2d(tris) / 2


def random_convex_hull_with_points(n: int, m: int, rng=None) -> ConvexHull:
    """
    Generate random convex hull with n points on the hull and m points inside
    the hull.
    """
    assert n >= 3, 'n must be greater than or equal to 3'
    assert m >= 0, 'm must be greater than or equal to 0'
    rng = np.random.default_rng() if rng is None else rng
    hull = random_convex_hull(n, rng=rng)
    tri = Delaunay(hull.points[hull.vertices])
    points = random_points_in_delaunay(tri, m, rng=rng)
    return ConvexHull(rng.permutation(np.concatenate((hull.points, points))))


def main():
    n, m = 10, 100
    hull = random_convex_hull_with_points(n, m)
    mask = np.ones(len(hull.points), dtype=bool)
    mask[hull.vertices] = False
    plt.plot(*hull.points[hull.simplices].T, 'k-')
    plt.plot(*hull.points[mask, :].T, 'o', lw=2)
    plt.plot(*hull.points[~mask, :].T, 'o', lw=2)
    plt.axis('equal')
    plt.show()


if __name__ == '__main__':
    main()
