import numpy as np
import scipy as sp
from scipy.sparse import spdiags
from scipy.sparse.linalg import spsolve

def adv_diff(D, w, years, L=30, phi=1, dx=0.1, dt=0.001, bc_top=1):
    """Solver for AD PDE equation"""
    N = int(L / dx) + 1

    [AL, AR] = AL_AR_dirichlet(D, w, phi, dt, dx, N)

    res = np.zeros((N))
    res[0] = bc_top

    yield res

    for _ in range(int(years / dt)):
        res = sp.sparse.linalg.spsolve(AL, AR.dot(res), use_umfpack=True)
        res[0] = bc_top
        yield res


def AL_AR_dirichlet(D, w, phi, dt, dx, N):
    """AL_AR_dirichlet: creates AL and AR matrices with Dirichlet BC"""
    s = phi * D * dt / dx / dx  #
    q = phi * w * dt / dx  #
    e1 = np.ones((N, 1))  #
    AL = spdiags(np.concatenate((e1 * (-s / 2 - q / 4), e1 * (1 + s), e1 * (-s / 2 + q / 4)), axis=1).T, [-1, 0, 1], N, N, format='csc')
    AR = spdiags(np.concatenate((e1 * (s / 2 + q / 4), e1 * (1 - s), e1 * (s / 2 - q / 4)), axis=1).T, [-1, 0, 1], N, N, format='csc')
    AL[0, :2] = 1, 0
    AL[-1, -2:] = -s, 1 + s
    AR[0, :2] = 1, 0
    AR[-1, -2:] = s, 1 - s
    return AL, AR


if __name__ == '__main__':
    D = 0.5
    w = 3
    t = 10
    C = np.array(list(adv_diff(D, w, t)))

