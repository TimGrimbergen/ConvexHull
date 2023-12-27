import numpy as np
import matplotlib.pyplot as plt


def show_hull(points: np.ndarray, hull: np.ndarray) -> None:
    """
    Draw the convex hull of a set of points and show the plot.
    """
    _, ax = plt.subplots()
    hull = np.vstack((hull, hull[0]))
    ax.plot(points[:,0], points[:,1], 'o', ms=6)
    ax.plot(hull[:,0], hull[:,1], 'o-', ms=7)
    plt.show()
