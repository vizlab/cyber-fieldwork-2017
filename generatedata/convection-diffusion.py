import numpy as np
import json
import matplotlib.pyplot as plt


#Thermal diffusivity of steel
D = 40.
#plate size, mm
w = h = 10.
#intervals in x-, y- directions, mm
dx = dy = 0.1
Tcool, Thot = 300, 700

nx, ny = int(w/dx), int(h/dy)
dx2, dy2 = dx*dx, dy*dy
dt = 0.0000625 # 0.0000625= (dx2 * dy2 / (2 * D * (dx2 + dy2))) / 10 when D = 4

# Initial conditions - ring of inner radius r, width dr centred at (cx,cy) (mm)
r, cx, cy = 2, 5, 5
r2 = r**2

def do_right_timestep(u0, u, vx,vy):
    # Propagate with forward-difference in time, central-difference in space
    u[1:-1, 1:-1] = u0[1:-1, 1:-1] + D * dt * ((u0[2:, 1:-1] - 2*u0[1:-1, 1:-1] + u0[:-2, 1:-1])/dx2 + (u0[1:-1, 2:] - 2*u0[1:-1, 1:-1] + u0[1:-1, :-2])/dy2 )\
                -(dt * vx[1:-1, 1:-1] * (u0[2:, 1:-1] - u0[1:-1, 1:-1]) / dx) \
                -(dt * vy[1:-1, 1:-1] * ((u0[1:-1, 2:] - u0[1:-1, 1:-1])/ dy))
                # -(dt * vy[1:-1, 1:-1] * ((u0[1:-1, 2:] - u0[1:-1, 1:-1])/ dy))
    u0 = u.copy()
    return u0, u

def do_left_timestep(u0, u, vx, vy):
    # Propagate with forward-difference in time, central-difference in space
    u[1:-1, 1:-1] = u0[1:-1, 1:-1] + D * dt * ((u0[2:, 1:-1] - 2*u0[1:-1, 1:-1] + u0[:-2, 1:-1])/dx2 + (u0[1:-1, 2:] - 2*u0[1:-1, 1:-1] + u0[1:-1, :-2])/dy2 )\
                -(dt * vx[1:-1, 1:-1] * (u0[:-2, 1:-1] - u0[1:-1, 1:-1]) / dx) \
                -(dt * vy[1:-1, 1:-1] * ((u0[1:-1, :-2] - u0[1:-1, 1:-1])/ dy))
    u0 = u.copy()
    return u0, u

def do_up_timestep(u0, u, vx, vy):
    # Propagate with forward-difference in time, central-difference in space
    u[1:-1, 1:-1] = u0[1:-1, 1:-1] + D * dt * ((u0[2:, 1:-1] - 2*u0[1:-1, 1:-1] + u0[:-2, 1:-1])/dx2 + (u0[1:-1, 2:] - 2*u0[1:-1, 1:-1] + u0[1:-1, :-2])/dy2 )\
                -(dt * vx[1:-1, 1:-1] * (u0[1:-1, :-2] - u0[1:-1, 1:-1]) / dx) \
                -(dt * vy[1:-1, 1:-1] * ((u0[:-2, 1:-1] - u0[1:-1, 1:-1])/ dy))
    u0 = u.copy()
    return u0, u

def do_down_timestep(u0, u, vx, vy):
    # Propagate with forward-difference in time, central-difference in space
    u[1:-1, 1:-1] = u0[1:-1, 1:-1] + D * dt * ((u0[2:, 1:-1] - 2*u0[1:-1, 1:-1] + u0[:-2, 1:-1])/dx2 + (u0[1:-1, 2:] - 2*u0[1:-1, 1:-1] + u0[1:-1, :-2])/dy2 )\
                -(dt * vx[1:-1, 1:-1] * (u0[1:-1, 2:] - u0[1:-1, 1:-1]) / dx) \
                -(dt * vy[1:-1, 1:-1] * ((u0[2:, 1:-1] - u0[1:-1, 1:-1])/ dy))
    u0 = u.copy()
    return u0, u

#timeSteps
tSteps = 501


for key, direction in enumerate(['left', 'down', 'right', 'up']):
    functionName = "do_" + direction + "_timestep"
    u0 = Tcool * np.ones((nx, ny))
    u = u0
    vx = np.ones((nx, nx))* 0
    vy = np.ones((ny, ny))* 100
    dataList = []

    for i in range(nx):
        for j in range(ny):
            p2 = (i*dx-cx)**2 + (j*dy-cy)**2
            if p2 < r2:
                u0[i,j] = Thot

    for m in range(tSteps):
        u0, u = eval(functionName)(u0, u, vx, vy)
        if m % 10 == 0:
            dataList.append(u.tolist())

    filePath = './front/public/convection-diffusion' + str(key) + '.json'

    with open(filePath, 'w') as outfile:
        json.dump(dataList, outfile)
