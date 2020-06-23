import pandas as pd
import numpy as np
import os
in_file = "1584019163732344.pcd"
out_file = "output.pcd"
X_threshold = 3
Y_threshold = 2
Z_threshold = 2

points = pd.read_csv(in_file, sep=' ', skiprows=11, header=-1, prefix='X')

points = points[np.logical_and(points["X0"] < X_threshold, points["X0"] > -X_threshold)]
points = points[np.logical_and(points["X1"] < Y_threshold, points["X1"] > -Y_threshold)]
points = points[np.logical_and(points["X2"] < Z_threshold, points["X2"] > -Z_threshold)]

file = open(out_file, "w")

with open(in_file) as my_file:
    header = [next(my_file) for x in range(11)]

for st in header:
    if st.split()[0] == "WIDTH":
        st = "WIDTH " + str(len(points)) + "\n"
    if st.split()[0] == "POINTS":
        st = "POINTS " + str(len(points)) + "\n"
    file.write(st)
file.write(points.to_string(index=False, header=False))

file.close()

os.system("pcl_pcd2ply output.pcd output.ply")
