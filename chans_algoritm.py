import numpy as np
import math
import matplotlib.pyplot as plt

def chans_algorithm(points: list[tuple], m=None) -> list[tuple]:
    """
    Find the convex hull of a set of points using the chan's algorithm.
    References: ...
    
    """

    n = len(points)

    # Handle trivial cases
    if n <= 2: return points

    # number of subsets for partitioning the points, also equal to number of points on convex hull
    m = 3 if not m else m 

    # Subdivide points into groups of n/m (can be a implemented more efficiently by creating a mapping instead of shuffling the array)
    points = np.random.shuffle(points)
    groups = [[] for _ in range(math.ceil(n/m))]
    for i in range(n):
        groups[i//m].append(points[i])
        
    # DEBUG: plot the groups
    plt.figure()
    for i in range(len(groups)):
        plt.scatter(groups)
    plt.show()

    return points