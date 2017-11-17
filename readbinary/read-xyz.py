# encoding: utf-8

import numpy as np
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
from scipy import genfromtxt


# length of head is 16 bytes
head = ("head","<i")
tail = ("tail","<i")

dt = np.dtype([head, ("data","float32")])
# fd = open('./Ra10^0/x3ds.bin', 'r')
fd = open('./681/B/x3ds.bin', 'r')
# chunk = np.fromfile(fd, dtype=dt, count=1)
chunk = np.fromfile(fd, dtype=dt)
data = chunk["data"]

# cut 4 bytes
data = data[2:]

data_len = len(data)
xyz_len = data_len / 3

x = []
y = []
z = []

for (i, scalar) in enumerate(data):
    xyz_idx = int(i / xyz_len)
    if xyz_idx == 2:
        x.append(scalar)
    elif xyz_idx == 1:
        y.append(scalar)
    elif xyz_idx == 0:
        z.append(scalar)

# for (X, Y, Z) in zip(x, y, z):
#     print(X, Y, Z)


# グラフ作成
fig = pyplot.figure()
ax = Axes3D(fig)

# 軸ラベルの設定
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Z-axis")

# 表示範囲の設定
# ax.set_xlim(4, 8)
# ax.set_ylim(2, 5)
# ax.set_zlim(1, 8)


# グラフ描画
ax.plot(x, y, z, "o", color="#cccccc", ms=4, mew=0.5)
pyplot.show()