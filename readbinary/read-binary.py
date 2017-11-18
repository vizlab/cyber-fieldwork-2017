# encoding: utf-8

import numpy as np
import matplotlib
from matplotlib import pyplot
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import genfromtxt


# length of head is 16 bytes
head = ("head","<i")

dt = np.dtype([head, ("data","float32")])

# fd = open('./Ra10^0/x3ds.bin', 'r')
fd = open('./681/B/x3ds.bin', 'r')
chunk = np.fromfile(fd, dtype=dt)
xyz_data = chunk["data"]

fd = open('./681/B/u3ds.bin', 'r')
chunk = np.fromfile(fd, dtype=dt)
uvwp_data = chunk["data"]

# cut 4 bytes
xyz_data = xyz_data[2:]
uvwp_data = uvwp_data[4:]
# print(len(xyz_data), len(uvwp_data))
xyz_len = len(xyz_data) // 3

x = [] # represented as x1 in the paper
y = [] # represented as x2 in the paper
z = [] # represented as x3 in the paper
u = uvwp_data[:xyz_len]
v = uvwp_data[xyz_len : xyz_len * 2]
w = uvwp_data[xyz_len * 2 : xyz_len * 3]
p = uvwp_data[xyz_len * 3 : xyz_len * 4]

for (i, scalar) in enumerate(xyz_data):
    xyz_idx = int(i / xyz_len)
    if xyz_idx == 0:
        x.append(scalar)
    elif xyz_idx == 1:
        y.append(scalar)
    elif xyz_idx == 2:
        z.append(scalar)

# get x-y surface (z=0) only
z0 = z[0]
for (i, z_scalar) in enumerate(z):
    if z_scalar != z0:
        z0_len = i - 1
        break
# draw graph
fig = pyplot.figure()
ax = Axes3D(fig)

# set range
ax.set_xlim(-0.5, 1.5)
ax.set_ylim(-0.5, 1.5)

# set labels
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Z-axis")

ax.plot(x[:z0_len], y[:z0_len], p[:z0_len], "o", color="#cccccc")
pyplot.show()

# create 2d array for plot
# u = []
# for (idx, i) in enumerate(x[:z0_len]):
#     u.append([])
#     for j in y[:z0_len]:
#         u[idx].append(j)
