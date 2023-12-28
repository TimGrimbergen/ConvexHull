import numpy as np
import math
import matplotlib.pyplot as plt

from show_hull import show_hull, show_hulls
from random_convex_hull import random_convex_hull_with_points
from graham_scan import graham_scan

np.random.seed(0)

def left_of(a: tuple, b: tuple, c: tuple) -> bool:
    """
    Check if point c is left of the line from a to b.
    """
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) > 0

def chan(points: list[tuple], m=None):
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
    np.random.shuffle(points)
    groups = [[] for _ in range(math.ceil(n/m))]
    for i in range(n):
        groups[i//m].append(points[i])

    # DEBUG: plot the groups
    #plt.figure()
    #for i in range(len(groups)):
    #    plt.scatter( [groups[i][j][0] for j in range(len(groups[i]))],
    #                 [groups[i][j][1] for j in range(len(groups[i]))],
    #                 s = 10
    #                 )
    #plt.show()

    # Compute the convex hulls of the groups with Graham's scan
    hulls = []
    for i in range(len(groups)):
        hulls.append(graham_scan(groups[i]))
    
    # Create look_up table for every point
    look_up = {}
    for i in range(len(hulls)):
        for j in range(len(hulls[i])):
            look_up[hulls[i][j]] = (i,j)

    # DEBUG: plot the subhulls
    show_hulls([np.array(groups[i]) for i in range(len(groups))], [np.array(hulls[j]) for j in range(len(hulls))])

    # Compute the total convex hull with Jarvis march
    hull = []
    point_on_hull = min(points)
    hull.append(point_on_hull)
    #illegal = set() # maintain a set that stores the points already on the convex hull

    for _ in range(m-1): # we need to add m-1 more points to the hull

        cur_hull, cur_ind = look_up[point_on_hull]
        #illegal.add(point_on_hull)

        # Now for each group, we need the "steepest tangent", i.e., we need to find the vertices of the subhulls
        # such that all other vertices of the subhulls lie on the left side.
        # Since the subhulls are stored in clockwise sorted order, we can perform binary search to do this.
        extreme_points = []
        for i in range(len(hulls)):
            if i == cur_hull: continue # current group is handled later

            ''' todo: fix binary search
            l, r = 0, len(hulls[i]) - 1 # handle cases where r <= 2 separately. Also, what if we encounter the current point_on_hull

            while l < r:
                m = l + (r-l)//2
                if hulls[i][m] in illegal: m_ = m+1

                # check if current m is correct, i.e., all points of the subhull must lie to the left of the line through 
                # the previous point on the hull and the new candidate. Note, if the two points adjacent to the candidate point
                # both lie to the left, we are done.
                if left_of(point_on_hull, hulls[i][m], hulls[i][m-1]) and left_of(point_on_hull, hulls[i][m], hulls[i][m+1]):
                    break

                elif not left_of(point_on_hull, hulls[i][m], hulls[i][m-1]): #check whether this makes sense
                    r = m
                else: #check whether this makes sense
                    l = m + 1

            extreme_points.append(hulls[i][m])
            '''

            # with linear scan
            for j in range(len(hulls[i])):
                if left_of(point_on_hull, hulls[i][j], hulls[i][j-1]) and left_of(point_on_hull, hulls[i][j], hulls[i][(j+1)%len(hulls[i])]):
                    extreme_points.append(hulls[i][j])
                    break

        # Now scan the extreme points, and pick the one that is most extreme.
        temp = hulls[cur_hull][cur_ind-1]
        for j in range(len(extreme_points)):
            if left_of(point_on_hull, extreme_points[j], temp):
                temp = extreme_points[j]

        point_on_hull = temp
        hull.append(point_on_hull)

    print(len(hull))
    return hull


def main():
    n, m = 5, 15
    points = random_convex_hull_with_points(n, m).points.tolist()
    points = [tuple(points[i]) for i in range(n+m)]
    hull = chan(points, n)
    show_hull(np.array(points), np.array(hull))


if __name__ == '__main__':
    main()