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
    #plt.savefig(f"figs/hull")
    #plt.show()

def show_hulls(groups: [np.ndarray], hulls: [np.ndarray]) -> None:
    """
    Draw the convex hull of a set of points and show the plot on a given figure f
    """
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    _, ax = plt.subplots()
    for i in range(len(groups)):
        hull = np.vstack((hulls[i], hulls[i][0]))
        ax.plot(groups[i][:,0], groups[i][:,1], 'o', ms=6, c = colors[i%len(colors)])
        ax.plot(hull[:,0], hull[:,1], 'o-', ms=7, c = colors[i%len(colors)])
    plt.savefig(f"figs/subhulls{len(hulls)}")
