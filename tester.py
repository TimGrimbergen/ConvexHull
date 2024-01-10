import numpy as np
try:
    from termcolor import colored
except:
    print("pip install termcolor for color coded messages!")

from create_hulls import load_hulls
from chans_algorithm import chan
from graham_scan import graham_scan
from gift_wrapping import gift_wrapping

def verify_hull(true_hull, candidate_hull):
    if len(true_hull) != len(candidate_hull): return False
    try: 
        return set(true_hull) == set(candidate_hull)
    except:
        return False

def test_algorithm(algorithm, folder):
    # given an algorithm (function from [tuple(x,y)] -> [tuple(x,y)]) and a folder with test cases this function checks if 
    # the algorithm yields the same convex hull vertices as the true_hull for the test case (according to scipy.spatial.ConvexHull)

    hulls = load_hulls(folder)

    for (n,m) in hulls:
        for id in hulls[(n,m)]:
            (hull, points) = ([tuple(x) for x in hulls[(n,m)][id]['hull'].tolist()], 
                              [tuple(x) for x in hulls[(n,m)][id]['points'].tolist()])
            my_hull = algorithm(points)
            if verify_hull(hull, my_hull):
                try:
                    print(colored(f"Check PASSED for id: {id}", color='green'))
                except:
                    print()
            else:
                try:
                    print(colored(f"Check FAILED for id: {id}", color='red'))
                except:
                    print()



if __name__ == '__main__':
    #run tests
    test_algorithm(graham_scan, './special_hulls')