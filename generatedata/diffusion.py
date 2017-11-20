import numpy as np
import json, codecs

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
#  u[1:-1, 1:-1] = np.empty((nx-2, ny-2))

#Initial conditions - ring of inner radius r, width dr centred at (cx, cy)(mm)
r, cx, cy = 2, 5, 5
r2 = r**2

#init conditions
for i in range(nx):
    for j in range(ny):
        p2 = (i*dx-cx)**2 + (j*dy-cy)**2
        if p2 < r2:
            u0[i, j] = Thot

#main algorithm
def do_timestep(u0, u):
    u[1:-1, 1:-1] = u0[1:-1, 1:-1] + D * dt * (
          (u0[2:, 1:-1] - 2*u0[1:-1, 1:-1] + u0[:-2, 1:-1])/dx2
          + (u0[1:-1, 2:] - 2*u0[1:-1, 1:-1] + u0[1:-1, :-2])/dy2 )

    u0 = u.copy()
    return u0, u

#timeSteps
tSteps = 501

dataList = []

for time in range(tSteps):
    u0, u = do_timestep(u0, u)
    if time % 10 == 0:
        dataList.append(u.tolist())

filePath = './front/public/diffusion.json'

with open(filePath, 'w') as outfile:
    json.dump(dataList, outfile)
