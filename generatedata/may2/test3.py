import numpy as np
import matplotlib.pyplot as plt

D = 1e-3
u = 0.15
v = 0.02

lx = 1.0
ly = 1.0
[x, y] = np.meshgrid(np.linspace(0, lx, 50), np.linspace(0, ly, 50))
dx = 0.1
dy = 0.1
dx2, dy2 = dx*dx, dy*dy
dt = dx2 * dy2 / (2 * D * (dx2 + dy2))  #
F = (((x - 0.3) ** 2 + (y - 0.3) ** 2) <= 0.1 ** 2)  #

rows = [i for i in range(50)]
cols = [i for i in range(50)]
[cols, rows] = np.meshgrid(cols, rows)

def mystencil(row, col):
    up = row + 1
    down = row - 1
    left = col - 1
    right = col + 1

    Dx = D * (F(row, left) - 2 * F(row, col) + F(row, right)) / (dx ** 2)
    Dy = D * (F(down, col) - 2 * F(row, col) + F(up, col)) / (dy **2)
    if (u >= 0):
        fu = u * (F(row, col) - F(row, left)) / dx
    else:
        fu = u * (F(row, right) - F(row, col)) / dx

    if (v >= 0):
        fv = v * (F(row, col) - F(down, col)) / dy
    else:
        fv = v * (F(up, col) - F(row, col)) / dy

    fn = F(row, col) + (Dx + Dy - (fu + fv)) * dt
    return row,col

def boundary(row, col):
    if (row == 1):
            fn = mystencil(49, col)
    elif (row == 50):
            fn = mystencil(2,col)
    else:
        if (col == 1):
                fn = mystencil(row,49)
        elif (col == 50):
                fn = mystencil(row,2)
        else:
                fn = mystencil(row,col)
    return row,col

X = np.zeros((50, 50, 50))


nsteps = 101

mfig = [0,20,50,100]
fignum = 0
fig = plt.figure()
for m in range(nsteps):
    X[:][:][1] = (((x - 0.3) ** 2 + (y - 0.3) ** 2) <= 0.2 ** 2)
   # print(rows[0],cols[0])
    Ft=[mystencil(row,col) for (row,col) in zip(rows, cols)]
    Fn=[boundary(row,col) for (row,col) in zip(rows, cols)]
    X[:][:][1] = Fn
    F = Fn
    if m in mfig:
        fignum += 1
        print(m, fignum)
        ax = fig.add_subplot(220 + fignum)
        im = ax.imshow(X, cmap=plt.get_cmap('hot'))
        ax.set_axis_off()
        ax.set_title('{:.1f} ms'.format(m*dt*1000))
fig.subplots_adjust(right=0.85)
cbar_ax = fig.add_axes([0.9, 0.15, 0.03, 0.7])
cbar_ax.set_xlabel('$T$ / K', labelpad=20)
fig.colorbar(im, cax=cbar_ax)
plt.show()