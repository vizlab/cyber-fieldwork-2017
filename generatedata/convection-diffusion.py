import numpy as np
import json
import matplotlib.pyplot as plt


#Thermal diffusivity of steel
D = 4.
#plate size, mm
w = h = 10.
#intervals in x-, y- directions, mm
dx = dy = 0.1
Tcool, Thot = 300, 700

nx, ny = int(w/dx), int(h/dy)
dx2, dy2 = dx*dx, dy*dy
dt = dx2 * dy2 / (2 * D * (dx2 + dy2))

u0 = Tcool * np.ones((nx, ny))
u = u0
vx = np.ones((nx, nx))* 0
vy = np.ones((ny, ny))* 10
print(vx, vy)
# Initial conditions - ring of inner radius r, width dr centred at (cx,cy) (mm)
r, cx, cy = 2, 5, 5
r2 = r**2

for i in range(nx):
    for j in range(ny):
        p2 = (i*dx-cx)**2 + (j*dy-cy)**2
        if p2 < r2:
            u0[i,j] = Thot

def do_timestep(u0, u, vx,vy):
    # Propagate with forward-difference in time, central-difference in space
    u[1:-1, 1:-1] = u0[1:-1, 1:-1] + D * dt * ((u0[2:, 1:-1] - 2*u0[1:-1, 1:-1] + u0[:-2, 1:-1])/dx2 + (u0[1:-1, 2:] - 2*u0[1:-1, 1:-1] + u0[1:-1, :-2])/dy2 )\
                -(dt * vx[1:-1, 1:-1] * (u0[2:, 1:-1] - u0[1:-1, 1:-1]) / dx) \
                -(dt * vy[1:-1, 1:-1] * ((u0[1:-1, 2:] - u0[1:-1, 1:-1])/ dy))
                # -(dt * vy[1:-1, 1:-1] * ((u0[1:-1, 2:] - u0[1:-1, 1:-1])/ dy))
    u0 = u.copy()
    return u0, u


#timeSteps
tSteps = 501
dataList = []

# Output 4 figures at these timesteps
mfig = [0, 20,40,60,80,90, 100,110,120]
fignum = 0
fig = plt.figure()
for m in range(tSteps):
    u0, u = do_timestep(u0, u, vx, vy)
    if m % 10 == 0:
        dataList.append(u.tolist())
    if m in mfig:
        fignum += 1
        print(m, fignum)
        ax = fig.add_subplot(330 + fignum)
        im = ax.imshow(u.copy(), cmap=plt.get_cmap('hot'), vmin=Tcool,vmax=Thot)
        ax.set_axis_off()
        ax.set_title('{:.1f} ms'.format(m*dt*1000))
fig.subplots_adjust(right=0.85)
cbar_ax = fig.add_axes([0.9, 0.15, 0.03, 0.7])
cbar_ax.set_xlabel('$T$ / K', labelpad=20)
fig.colorbar(im, cax=cbar_ax)
plt.show()

filePath = './front/public/convection-diffusion.json'

with open(filePath, 'w') as outfile:
    json.dump(dataList, outfile)
