import numpy as np
import math
import matplotlib.pyplot as plt

from show_hull import show_hull, show_hulls
from random_convex_hull import random_convex_hull_with_points
from graham_scan import graham_scan

np.random.seed(0)

def left_of(a: tuple, b: tuple, c: tuple) -> bool:
    """
    Returns 1 if point c is left of the line from a to b, 0 if c is on the line and -1 if right of the line
    """
    val =  (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    if val == 0: return 0
    return 1 if val > 0 else -1

def binary_search_hull(hull, point):
    """
    Finds the vertex of a convex hull such that all other points of the hull lie to the right of the directed line from point to that vertex 
    """
    l, r = 0, len(hull) - 1

    if r == 0: return hull[0]
    if r == 1: return hull[1] if left_of(point, hull[0], hull[1])==1 else hull[0]
    if point == hull[-1]: return hull[0] # hmm

    while l <= r: # verify if this REALLY works
        m = l + (r-l)//2

        if (left_of(point, hull[m], hull[m-1]) == -1 and left_of(point, hull[m], hull[(m+1)%(len(hull))]) == -1) or l == r:
            return hull[m]

        if left_of(point, hull[(m+1)%len(hull)], hull[m]) == 1 and left_of(point, hull[r], hull[m]) == 1:
            r = m
        elif left_of(point, hull[r], hull[m]) == -1:
            if left_of(point, hull[r], hull[l]) == -1:
                l = m + 1
            else:
                r = m
        else:
            l = m + 1
    
    return hull[m]

def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

#@profile # first: kernprof -l chans_algorithm.py ||  then: python3 -m line_profiler "chans_algorithm.py.lprof"
def chan(points: list[tuple], m=None):
    """
    Find the convex hull of a set of points using the chan's algorithm.
    References: ...
    
    """

    n = len(points)

    # Handle trivial cases
    if n <= 2: return points

    # number of subsets for partitioning the points, also equal to number of points on convex hull
    m = 5 if not m else m 
    #np.random.shuffle(points)

    while True:
        # Subdivide points into groups of size n/m
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
            cur_hull = graham_scan(groups[i])
            hulls.append(cur_hull)
            
        # Create look_up table for every point (not really necessary, can also do without I think)
        look_up = {}
        for i in range(len(hulls)):
            for j in range(len(hulls[i])):
                look_up[hulls[i][j]] = (i,j)

        # DEBUG: plot the subhulls
        #show_hulls([np.array(groups[i]) for i in range(len(groups))], [np.array(hulls[j]) for j in range(len(hulls))])

        # Compute the total convex hull
        hull = []
        point_on_hull = min(points) # add left-most point
        hull.append(point_on_hull)

        while True: # we need to add m-1 more points to the hull
            cur_hull, cur_ind = look_up[point_on_hull]
            cur_most_extreme = hulls[cur_hull][(cur_ind+1)%len(hulls[cur_hull])] # for current hull, next candidate is always just the next clockwise point

            # Now for each group, we need the "steepest tangent", i.e., we need to find the vertices of the subhulls such that all
            # other vertices of the subhulls lie on the right side of the directed line from last convex hull point to the new vertex.
            # Since the subhulls are stored in clockwise sorted order, we can perform binary search to do this.
            extreme_points = []
            for i in range(len(hulls)):
                if i == cur_hull: continue #handled separately

                #binary search for next point on every hull
                cur_extreme_point = binary_search_hull(hulls[i], point_on_hull) # this sorta work

                is_right = left_of(point_on_hull, cur_extreme_point, cur_most_extreme)

                if is_right == -1 or (is_right == 0 and dist(cur_extreme_point, point_on_hull) > dist(cur_most_extreme, point_on_hull)):
                    cur_most_extreme = cur_extreme_point

                #print(look_up[cur_extreme_point])
                #extreme_points.append(cur_extreme_point)

            # Now scan the extreme points, and pick the one that is most extreme (i.e. most "clockwise").
            #temp = hulls[cur_hull][(cur_ind+1)%len(hulls[cur_hull])]
            #for p in extreme_points:
            #    if left_of(point_on_hull, p, temp) <= 0:
            #        temp = p

            #point_on_hull = temp
            point_on_hull = cur_most_extreme

            if point_on_hull == hull[0]: 
                #print(len(hull))
                return hull

            hull.append(point_on_hull)

            if len(hull) >= m:
                #print(f"Couldn't find hull of size {m}, will now try with {m*m}")
                break

        m = m*m
        
        #for the new points only select those that were part of a convex hull
        if m > 3:
            points = [hulls[i][j] for i in range(len(hulls)) for j in range(len(hulls[i]))]
            n = len(points)


def main():
    n, m = 26, 10000
    true_hull = random_convex_hull_with_points(n, m)
    all_points = true_hull.points.tolist()
    points = [tuple(all_points[i]) for i in range(n+m)]
    true_hull_points = [tuple(x) for x in true_hull.points[true_hull.vertices].tolist()]
    my_hull = chan(points, None) # important line
    #show_hull(np.array(points), np.array(my_hull))

    #print(my_hull)
    #for i in range(len(my_hull)):
    #    if i == 0: print(my_hull[i])
    #    x = binary_search_hull(my_hull, my_hull[i])
    #    x = my_hull[(i+1)%len(my_hull)]
    #    y = my_hull[(i)%len(my_hull)]
    #   show_hull(np.array(points), np.array(my_hull))
    #    plt.plot([x[0], y[0]], [x[1], y[1]], color='red', linewidth=5)
    #    plt.show()


if __name__ == '__main__':
    main()