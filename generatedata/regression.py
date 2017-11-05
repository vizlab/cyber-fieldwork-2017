import numpy as np
import json, codecs
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
reg = linear_model.LinearRegression()

filePath = '../front/public/data.json'

with open(filePath, 'r') as readfile:
    data_json = json.load(readfile)
scalar_fields = np.array(data_json, np.float32)

dt = 0.0006250000000000001*10 #sec
dx = 0.1 #m
dy = 0.1 #m
#配列サイズ 51*100*100
f_t = np.gradient(scalar_fields, axis=0)/dt
f_x = np.gradient(scalar_fields, axis=1)/dx
f_y = np.gradient(scalar_fields, axis=2)/dy
f_xx = np.gradient(f_x, axis=1)/dx
f_yy = np.gradient(f_y, axis=2)/dy

#配列サイズチェック
# print('scalar_fields',scalar_fields.shape)
# print('f_t',f_t.shape)
# print('f_x',f_x.shape)
# print('f_y',f_y.shape)
# print('f_xx',f_xx.shape)
# print('f_yy',f_yy.shape)

###gradientチェック用グラフ###
# plt.figure()
# # 矢印（ベクトル）の始点
# X = []
# Y = []
# for i in range(100):
#     for j in range(100):
#         X.append(i)
#         Y.append(j)
# # 矢印（ベクトル）の成分
# U = f_x[3,:,:].flatten()
# V = f_y[3,:,:].flatten()
# # 矢印（ベクトル）
# plt.quiver(X,Y,U,V,angles='xy',scale_units='xy',scale=10)
# # グラフ表示
# plt.xlim([0,100])
# plt.ylim([0,100])
# plt.grid()
# plt.draw()
# plt.show()

#回帰分析できる形に変形
# f = scalar_fields.flatten()
# f_t_col = f_t.flatten()
# f_x_col = f_x.flatten()
# f_y_col = f_y.flatten()
# f_xx_col = f_xx.flatten()
# f_yy_col = f_yy.flatten()
# partial = np.c_[f_xx_col, f_yy_col, f, f_x_col, f_y_col]

#回帰分析変数を最低限に
f_t_col = f_t.flatten()
f_xx_col = f_xx.flatten()
f_yy_col = f_yy.flatten()
partial = np.c_[f_xx_col, f_yy_col]

###一部の範囲で回帰分析してみるとD=4でちゃんと結果がでる
# f_t_col = f_t[:,40:60,40:60].flatten()
# f_xx_col = f_xx[:,40:60,40:60].flatten()
# f_yy_col = f_yy[:,40:60,40:60].flatten()
# partial = np.c_[f_xx_col, f_yy_col]

#配列サイズ確認
#print('f',f.shape)
print('f_t_col',f_t_col.shape)
#print('f_x_col',f_x_col.shape)
#print('f_y_col',f_y_col.shape)
print('f_xx_col',f_xx_col.shape)
print('f_yy_col',f_yy_col.shape)
print('partial',partial.shape)

#予測モデル
reg.fit(partial,f_t_col)

#回帰係数
print(pd.DataFrame({"Name":['f_xx', 'f_yy'],#, 'f', 'f_x', 'f_y'],
                    "Coefficients":reg.coef_}).sort_values(by='Coefficients'))
print(reg.intercept_)
print(reg.score(partial, f_t_col))

###  D=4.になるはず
###Q.なぜ結果が少しずれるのか？
###     データが少ない？
###     座標が2次元のせいで初期値が2次元で存在してるのがうまくいかない理由？
###     初期値700の範囲に対してのみ回帰分析を行なった結果D=4が求められた
###     それなら係数自体はどの座標点でとっても一定になるはず？
