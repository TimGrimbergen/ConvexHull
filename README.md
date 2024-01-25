# Convex Hull Algorithm implementations

This is a project that was done for the course Geometric Algorithms at Utrecht University. 
We implemented three convex hull algorithms: Jarvis March, Graham Scan and Chan's algorithm.

## Getting Started

Simply clone this repository and pip install all required dependencies: numpy, matplotlib, random and scipy. 

## Test scripts & Test cases

Several test scripts and test cases are created to analyze the correctness and performance of the various algorithms.

The test cases are divided in two groups: randomly generated hulls and "special" hulls. The special hulls contain configurations
where multiple (almost) points lie on the same line.

The following command checks the correctness of the algorithms:
```
python3 tester.py
```
The folder should be entered in the script itself and should contain subfolders with names "k_n", where $k$ is the number of vertices on the
convex hull and $n$ is the number of points in the interior. Inside each subfolder "k_n", two files should be provided, one storing the coordinates of
the hull vertices and one storing the interior points. These files are named "hull\_123456789" and "points\_123456789" respectively. Multiple of these 
combinations can exist in one subdirectory but the 9 digit codes should be unique for different test cases.

The following command can be used to time the algorithms:
```
python3 run_tests.py
```
The algorithms and folder containing the hulls should again be provided in the script itself.

```
python3 create_hulls.py
```
This script can be used to generate test cases. In the script, set a folder to which the test cases will be saved in the format as stated above. 
For creating hulls there are two functions: `create_hulls` and `create_special_hull`. The former will generate random convex hulls and the latter
requires the hull vertices and points to be entered manually.


## Authors

* **Tim Grimbergen** (t.grimbergen@students.uu.nl)
* **Timo Post** (t.f.post@students.uu.nl)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
