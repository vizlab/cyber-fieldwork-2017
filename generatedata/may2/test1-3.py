from asyncio import gather

# import drawnow as drawnow
import matplotlib.pyplot as plt
# from numpy import meshgrid, linspace
import numpy as np


def adv_dif_2d(Usegpu, mesh_size, t):
    D = 1e-3  # 拡散係数
    u = 0.15  # x方向の速度
    v = 0.02  # y方向の速度

    lx = 1.0  # 計算領域の全長(x)
    ly = 1.0  # 計算領域の全長(y)
    [x, y] = np.meshgrid(np.linspace(0, lx, mesh_size), np.linspace(0, ly, mesh_size))  # 座標マップを作成
    dx = x[1, 2] - x[1, 1]  # 1マス間の距離を計算(x)
    dy = y[2, 1] - y[1, 1]  # 1マス間の距離を計算(y)
    dt = t[2] - t[1]  # 1ステップあたりの時間間隔を計算

    F = (((x - 0.3) ** 2 + (y - 0.3) ** 2) <= 0.1 ** 2)  # 初期条件は(0.3, 0.3)を中心とした半径0.1の円の内部が1になるように指定
    rows = [i for i in range(mesh_size)]
    cols = [i for i in range(mesh_size)]
    [cols, rows] = np.meshgrid(cols, rows)

    # 関数定義
    def mystencil(row, col):  # 上下左右のインデックスを計算
        up = row + 1
        down = row - 1
        left = col - 1
        right = col + 1

        # 拡散項(2次精度中心差分法)
        Dx = D * (F(row, left) - 2 * F(row, col) + F(row, right)) / (dx ^ 2)
        Dy = D * (F(down, col) - 2 * F(row, col) + F(up, col)) / (dy ^ 2)

        # 移流項(1次精度風上差分法)
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

    def GetFt(rows, cols):
        Rows = np.array(rows)
        Cols = np.array(cols)
        Rows.reshape(mesh_size ** 2)
        Cols.reshape(mesh_size ** 2)
        ft = []
        for row, col in zip (Rows, Cols):
            ft.append(mystencil(row, col))

        ft = np.array(ft)
        return list(ft.reshape(mesh_size, mesh_size))

    def boundary(row, col):  # 境界の処理
        if (row == 1):
            fn = Ft[mesh_size - 1][col]
        elif (row == mesh_size):
            fn = Ft[2][col]
        else:
            if (col == 1):
                fn = Ft[row][mesh_size - 1]
            elif (col == mesh_size):
                fn = Ft[row][2]
            else:
                fn = Ft[row][col]
        return row,col

    def GetFn(rows, cols):
        Rows = np.array(rows)
        Cols = np.array(cols)
        Rows.reshape(mesh_size ** 2)
        Cols.reshape(mesh_size ** 2)
        fnx = []
        for row, col in zip(Rows, Cols):
            fnx.append(boundary(row, col))
            return list(fnx.reshape(mesh_size, mesh_size))

    # メイン処理
    timer = plt.figure()
    print(x.shape[1])
    X = np.zeros((50, 50, 50))

    X[:][:][1] = (((x - 0.3) ** 2 + (y - 0.3) ** 2) <= 0.2 ** 2)

    m = 1
    for i in t[1:]:
        Ft = GetFt(rows, cols)
        Fn = GetFn(rows, cols)
        X[m][:][0] = Fn
        m += 1
        F = Fn


X = adv_dif_2d(0, 50, [i / 10 for i in range(51)])

