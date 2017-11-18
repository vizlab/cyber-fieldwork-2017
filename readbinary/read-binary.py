# encoding: utf-8

import numpy as np
import json
import matplotlib
from matplotlib import pyplot
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

data_list = []  # this array is saved as json

# length of head is 16 bytes
head = ("head","<i")

dt = np.dtype([head, ("data","float32")])

# fd = open('./Ra10^0/x3ds.bin', 'r')
fd = open('./readbinary/data/993/non-B/x3ds.bin', 'r')
chunk = np.fromfile(fd, dtype=dt)
xyz_data = chunk["data"]

fd = open('./readbinary/data/993/non-B/u3ds.bin', 'r')
chunk = np.fromfile(fd, dtype=dt)
uvwp_data = chunk["data"]

xyz_data = xyz_data[2:]         # cut 4 bytes
xyz_len = len(xyz_data) // 3    # xyz_len = number of data in each time step

# get xyz coordinates data
x = [] # represented as x1 in the paper
y = [] # represented as x2 in the paper
z = [] # represented as x3 in the paper
for (i, scalar) in enumerate(xyz_data):
    xyz_idx = int(i / xyz_len)
    if xyz_idx == 0:
        x.append(scalar)
    elif xyz_idx == 1:
        y.append(scalar)
    elif xyz_idx == 2:
        z.append(scalar)

for t in range(41):
    head_idx = 4 * (t + 1) + (xyz_len * 4) * t

    u = uvwp_data[head_idx               : head_idx + xyz_len]
    v = uvwp_data[head_idx + xyz_len     : head_idx + xyz_len * 2]
    w = uvwp_data[head_idx + xyz_len * 2 : head_idx + xyz_len * 3]
    p = uvwp_data[head_idx + xyz_len * 3 : head_idx + xyz_len * 4]

    if t == 0:
        # get x-y surface (z=0) only
        z0 = z[0]
        for (i, z_scalar) in enumerate(z):
            if z_scalar != z0:
                z0_len = i
                break

        # get sampling points of x coordinates
        x0 = x[0]
        for (i, x_scalar) in enumerate(x):
            if x_scalar == x0 and i != 0:
                n_x = i
                break

        # get sampling points of y coordinates and z_coordinates
        n_y = z0_len // n_x
        n_z = len(p) // n_x // n_y

    # create 2d array for plot
    p_3d = np.reshape(p, (n_z, n_y, n_x))
    p_zx = p_3d[:, 0, :]
    p_zx = p_zx.transpose() # shape is changed to u[x][z]

    # reduce data when save as json file
    data_list.append(p_zx[::2, :].tolist())


    if t % 10 == 0:
        x_coord = np.linspace(min(x), max(x), n_x)
        y_coord = np.linspace(min(y), max(y), n_y)
        z_coord = np.linspace(min(z), max(z), n_z)

        z_mesh, x_mesh = np.meshgrid(z_coord, x_coord)

        # draw 2d color plot
        ax = plt.subplot(1, 1, 1)
        ax.set_xlim(-0.5, 2.5)
        ax.set_ylim(-0.5, 2.5)
        plt.pcolor(z_mesh, x_mesh, p_zx, cmap='bwr', vmin=0, vmax=100)
        plt.title('pcolorfast')
        plt.colorbar()
        plt.show()

filePath = './front/public/lock-exchange-993-nonB.json'

with open(filePath, 'w') as outfile:
    json.dump(data_list, outfile)

# # draw 3d scatter
# fig = pyplot.figure()
# ax = Axes3D(fig)
#
# # set range
# ax.set_xlim(-0.5, 1.5)
# ax.set_ylim(-0.5, 1.5)
#
# # set labels
# ax.set_xlabel("X-axis")
# ax.set_ylabel("Y-axis")
# ax.set_zlabel("Z-axis")
#
# ax.plot(x[:z0_len:10], y[:z0_len:10], p[:z0_len:10], "o", color="#cccccc")
# pyplot.show()
