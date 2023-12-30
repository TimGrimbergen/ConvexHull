import numpy as np
import matplotlib.pyplot as plt


def show_hull(points: np.ndarray, hull: np.ndarray) -> None:
    """
    Draw the convex hull of a set of points and show the plot.
    """
    hull = np.vstack((hull, hull[0]))
    plt.plot(points[:,0], points[:,1], 'o', ms=6)
    plt.plot(hull[:,0], hull[:,1], 'o-', ms=7)
    plt.show()
