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

    #startLeftPrev = left_of(point, hull[l], hull[r])
    #startLeftNext = left_of(point, hull[l], hull[l+1])

    while l <= r: #should be more sophisticated
        m = l + (r-l)//2

        if left_of(point, hull[m], hull[m-1]) == -1 and left_of(point, hull[m], hull[(m+1)%(len(hull))]) == -1:
            return hull[m]

        if l == r:
            return hull[m]
        
        #if l == r: #weird case...
        #    # check if it should be the left or right neighbor of the current index
        #    if left_of(point, hull[(l+1)%(len(hull))], hull[l]) == -1 and left_of(point, hull[(l+1)%(len(hull))], hull[(l+2)%(len(hull))]) == -1:
        #        return hull[(l+1)%(len(hull))]
        #    elif left_of(point, hull[l-1], hull[l-2]) == -1 and left_of(point, hull[l-1], hull[(l)%(len(hull))]) == -1:
        #        return hull[l-1]
        #    else:
        #        raise RuntimeError(f"Binary search terminated at {l}, but it is not the correct point and neither are its neighbors")

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



    '''
    while True:
        m = l + (r-l)//2

        # check if current m is correct, i.e., all points of the subhull must lie to the left of the line through 
        # the previous point on the hull and the new candidate. Note, if the two points adjacent to the candidate point
        # both lie to the left, we are done.
        if (left_of(point, hull[m], hull[m-1]) and left_of(point, hull[m], hull[(m+1)%len(hull)])) or l == r:
            break
        
        #this does not make sense
        #elif not left_of(point, hull[m], hull[(m+1)%len(hull)]): #check whether this makes sense
        #    l = m + 1
        #else: #check whether this makes sense
        #    r = m
        
        # how to decide whether to replace l by m + 1 or r by m?
        # we want that the answer is one of the new points l..r
        # either all points from l..m or all points from m+1..r are not valid
        # for some reason the extra check on line 102 makes it work
        elif left_of(point, hull[m+1+(r-(m+1))//2], hull[l+(m-l)//2]):
            l = m + 1
        else:
            r = m
    '''

    # check if index 0 is the correct point, if yes select this point
    #if left_of(point, hull[0], hull[1]) and left_of(point, hull[0], hull[-1]):
    #    m = 0
    
    return hull[m]


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
    #np.random.shuffle(points)

    while True:
        # Subdivide points into groups of n/m (can be a implemented more efficiently by creating a mapping instead of shuffling the array)
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

        while True: # we need to add m-1 more points to the hull
            #print(point_on_hull)
            cur_hull, cur_ind = look_up[point_on_hull]
            #illegal.add(point_on_hull)

            # Now for each group, we need the "steepest tangent", i.e., we need to find the vertices of the subhulls
            # such that all other vertices of the subhulls lie on the left side.
            # Since the subhulls are stored in clockwise sorted order, we can perform binary search to do this.
            extreme_points = []
            for i in range(len(hulls)):
                if i == cur_hull: continue #handled separately

                cur_extreme_point = binary_search_hull(hulls[i], point_on_hull) # this does not work

                #print(look_up[cur_extreme_point])
                extreme_points.append(cur_extreme_point)
                
                #with linear scan (this works)

                #if len(hulls[i]) == 1: extreme_points.append(hulls[i][0])
                #if len(hulls[i]) == 2: extreme_points.append(hulls[i][1]) if left_of(point_on_hull, hulls[i][1], hulls[i][0]) == -1 else extreme_points.append(hulls[i][0])

                #for j in range(len(hulls[i])):
                #    if left_of(point_on_hull, hulls[i][j], hulls[i][j-1]) == -1 and left_of(point_on_hull, hulls[i][j], hulls[i][(j+1)%len(hulls[i])]) == -1:
                #        extreme_points.append(hulls[i][j])
                #        break

            # Now scan the extreme points, and pick the one that is most extreme (i.e. most "clockwise").
            temp = hulls[cur_hull][(cur_ind+1)%len(hulls[cur_hull])]
            for p in extreme_points:
                if left_of(point_on_hull, p, temp) <= 0:
                    temp = p

            point_on_hull = temp
            if point_on_hull == hull[0]: 
                print(len(hull))
                return hull

            hull.append(point_on_hull)

            if len(hull) >= m:
                print(f"Couldn't find hull of size {m}, will now try with {m*m}")
                break

        m = m*m


def main():
    n, m = 3, 100
    points = random_convex_hull_with_points(n, m).points.tolist()
    points = [tuple(points[i]) for i in range(n+m)]
    hull = chan(points, None)
    show_hull(np.array(points), np.array(hull))


if __name__ == '__main__':
    main()