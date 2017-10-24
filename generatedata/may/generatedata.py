import numpy as np
import matplotlib.pyplot as plt
import json, codecs

def main():
    #plate size, mm
    w = h = 10.

    #intervals in x-, y- directions, mm
    dx = dy = 0.1

    #Thermal diffusivity of steel
    D = 4.

    Tcool, Thot = 300, 700

    nx, ny = int(w/dx), int(h/dy)
    dx2, dy2 = dx*dx, dy*dy
    dt = dx2 * dy2 / (2 * D * (dx2 + dy2))

    u0 = Tcool * np.ones((nx, ny))
    u = np.empty((nx, ny))

    #Initial conditions - ring of inner radius r, width dr centred at (cx, cy)(mm)
    r, cx, cy = 2, 5, 5
    r2 = r**2

    for i in range(nx):
        for j in range(ny):
            p2 = (i*dx-cx)**2 + (j*dy-cy)**2
            if p2 < r2:
                u0[i, j] = Thot

    u0List = u0.tolist()
    filePath = '../../front/public/u0.json'

    with open(filePath, 'w') as outfile:
        json.dump(u0List, outfile)

if __name__ == "__main__":
    print("test")
    main()
