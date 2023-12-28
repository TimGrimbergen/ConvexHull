import numpy as np

from show_hull import show_hull
from random_convex_hull import random_convex_hull_with_points


def xyz_to_hex(c):
    cmap = {0 : "0", 1 : "1", 2 : "2", 3 : "3", 4 : "4", 5 : "5", 6 : "6", 7 : "7", 8 : "8", 9 : "9",
            10 : "A", 11 : "B", 12 : "C", 13 : "D", 14 : "E", 15 : "F"}
    x = "".join(cmap[s] for s in divmod(c[0], 16))
    y = "".join(cmap[s] for s in divmod(c[1], 16))
    z = "".join(cmap[s] for s in divmod(c[2], 16))
    return "#" + x + y + z


def cos_dot(p1, p2):
    # calculates the cosine of the angle with the dot-product formula, assumes p1 lies to the left of p2

    numerator =  (p2[0] - p1[0]) ** 2
    denominator = np.sqrt( (p2[0] - p1[0])**2 ) * np.sqrt( (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 )

    return numerator / denominator


def compute_angle(p1, p2): # returns cosine of angle
    if p1[1] == p2[1]:
        if p1[0] < p2[0]: return -1
        else: return 1 # this case does not happen since we pick the left-most starting point

    if p1[0] < p2[0]:
        return -cos_dot(p1, p2)
    elif p1[0] == p2[0]:
        return 0
    else:
        return cos_dot(p1, (p2[0] + 2*(p1[0] - p2[0]), p2[1]))


def sort_helper(p1, p2):
    if p1 == p2: return (10000,0) # we want the initial point (p1) to be last
    angle = compute_angle(p1, p2)
    dist = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    return -angle, -dist


def right_turn(stack):
    if len(stack) < 3: return True
    p,q,s = stack[-3], stack[-2], stack[-1]
    cross_z = (p[0] - q[0])*(s[1] - q[1]) - (p[1] - q[1])*(s[0] - q[0])
    return True if cross_z > 0 else False


def graham_scan(points):
    '''
        Input:
            - points [(float, float)] : list of points to calculate the convex hull of.

        Output:
            - points of the convex hull sorted in clockwise order
    '''
    # find lowest point, if several lowest points, pick the most left one
    p_start = min(points, key = lambda p : (p[1], p[0]))

    # sort points in order of polar angle with p_start. If several points with the same angle, sort by distance to p_start
    points.sort(key = lambda p : sort_helper(p_start, p))
    # return p_start, points # debug

    stack = []
    for i, p in enumerate(points):
        while len(stack) > 1 and not right_turn(stack + [p]):
            stack.pop()
        stack.append(p)

    return stack


# # test sorting
# if __name__ == '__main__':
#     #points = [(np.random.uniform(-10, 10), np.random.uniform(-9, 10)) for _ in range(100)] + [(0, -10)]
#     points = [(0,0), (1,1), (2,2), (3,3)]
#     colors = [( 0, 0, round(255 * x / len(points)) ) for x in range(len(points))]
#     colors = [xyz_to_hex(c) for c in colors]

#     plt.figure(1)
#     for i in range(len(points)):
#         plt.scatter(points[i][0], points[i][1], color=colors[i])
#     plt.show()

#     sorted_points = graham_scan(points)[1]
#     plt.figure(2)
#     for i in range(len(sorted_points)):
#         plt.scatter(sorted_points[i][0], sorted_points[i][1], color=colors[i])
#     plt.show()

def main():
    n, m = 10, 100
    points = random_convex_hull_with_points(n, m).points.tolist()
    hull = graham_scan(points)
    show_hull(np.array(points), np.array(hull))
    # print(hull)


if __name__ == '__main__':
    main()