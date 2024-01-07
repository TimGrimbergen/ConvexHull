import random
import numpy as np
import os

from random_convex_hull import random_convex_hull_with_points

save_folder = "./hulls"

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
    S_vals = [20, 40, 60, 80, 100, 200, 300, 400, 500]
    n = 20
    for S in S_vals:
        create_hulls(5, n, S-n, save_folder)
    
    #hulls = load_hulls(save_folder)
    #print(hulls[(5,15)]["980458186"]['hull'])

