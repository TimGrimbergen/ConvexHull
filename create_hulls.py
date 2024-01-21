import random
import numpy as np
import os

from random_convex_hull import random_convex_hull_with_points

def create_special_hull(points, hull, save_folder):
    n = len(hull)
    m = len(points) - n

    try:
        os.mkdir(f"{save_folder}/{n}_{m}")
        print(f"Saving hulls to existing directory: {save_folder}/{n}_{m}")
    except:
        print(f"Saving hulls to new directory: {save_folder}/{n}_{m}")

    id = random.randint(100_000_000, 999_999_990)
    np.savetxt(f"{save_folder}/{n}_{m}/points_{id}", points)
    np.savetxt(f"{save_folder}/{n}_{m}/hull_{id}", hull)


def create_hulls(N, n, m, save_folder):
    try:
        os.mkdir(f"{save_folder}/{n}_{m}")
        print(f"Saving hulls to existing directory: {save_folder}/{n}_{m}")
    except:
        print(f"Saving hulls to new directory: {save_folder}/{n}_{m}")

    for i in range(N):
        id = random.randint(100_000_000, 999_999_990)
        hull = random_convex_hull_with_points(n, m)
        np.savetxt(f"{save_folder}/{n}_{m}/points_{id}", [tuple(x) for x in hull.points.tolist()])
        np.savetxt(f"{save_folder}/{n}_{m}/hull_{id}", [tuple(x) for x in hull.points[hull.vertices].tolist()])

def load_hulls(folder, n = None, m = None):
    hulls = {} # store hulls as lists of pairs (poits, hull_points) by (n,m) key

    # if needed: make it so only directory (n,m) is selected given input n and m.
    for dir_name in os.listdir(folder):
        n, m = [int(x) for x in dir_name.split('_')]
        hulls[(n,m)] = {}
        for file in os.listdir(f"{folder}/{dir_name}"):
            id = file[-9:]
            if id not in hulls[(n,m)]: hulls[(n,m)][id] = {}

            if file[:4] == 'hull':
                hulls[(n,m)][id]['hull'] = np.loadtxt(f"{folder}/{n}_{m}/hull_{id}")
            elif file[:6] == 'points':
                hulls[(n,m)][id]['points'] = np.loadtxt(f"{folder}/{n}_{m}/points_{id}") 
            else:
                raise RuntimeError(f"Unexpcted file ({file}) appears in: {folder}/{dir_name}")
    
    return hulls

if __name__ == '__main__':
    #'''
    save_folder = "./hulls2"
    S_vals = [5,10,50,100,500,1000,3000, 6000, 10000, 25000, 50000, 100000]
    #n_vals = [10,50,100,500,1000,3000, 6000, 10000, 25000, 50000, 100000, 200000, 400000, 490000, 499500]
    n = 9
    #S = 500000
    for s in S_vals:
        create_hulls(10, n, s-n, save_folder)
    #for n in n_vals:
    #    create_hulls(3, n, S-n, save_folder)
    
    #hulls = load_hulls(save_folder)
    #print(hulls[(5,15)]["980458186"]['hull'])
    #'''
    '''
    points = [(0, 0), (1,0), (0.1, 0.1), (0.5, 0.5), (0.3, 0.3), (1, 0.5), (1, 0.3), (0.2, 0), (0.6, 0), 
              (1,1)]
    hull = [(0, 0), (1, 1), (1, 0)]

    create_special_hull(points, hull, "./special_hulls")
    '''

