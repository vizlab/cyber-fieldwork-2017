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

#配列サイズ 51*100*100
f_t = np.gradient(scalar_fields, axis=0)
f_x = np.gradient(scalar_fields, axis=1)
f_y = np.gradient(scalar_fields, axis=2)
f_xx = np.gradient(f_x, axis=1)
f_yy = np.gradient(f_y, axis=2)


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

# scalar_fields = scalar_fields - scalar_fields[0,:,:]
# print(scalar_fields[0,:,:])
# print(scalar_fields[50,:,:])

#回帰分析できる形に変形
f = scalar_fields.flatten()
f_t_col = f_t.flatten()
f_x_col = f_x.flatten()
f_y_col = f_y.flatten()
f_xx_col = f_xx.flatten()
f_yy_col = f_yy.flatten()
partial = np.c_[f_t_col, f_x_col, f_y_col, f_xx_col, f_yy_col]

###ある座標(x,y)でならちゃんと出そう？，でもそれだとサンプル少ない
###多数の点で回帰分析をして係数の平均を取るとか？
# f = scalar_fields[:,49,49].flatten()
# f_t_col = f_t[:,49,49].flatten()
# f_x_col = f_x[:,49,49].flatten()
# f_y_col = f_y[:,49,49].flatten()
# partial = np.c_[f_t_col, f_x_col, f_y_col]

###fを無くしてみる，ダメっぽい，むしろ微分項を増やすべき？###
# f = f_t_col
# partial = np.c_[f_x_col, f_y_col]

#配列サイズ確認
# print('f',f.shape)
# print('f_t_col',f_t_col.shape)
# print('f_x_col',f_x_col.shape)
# print('f_y_col',f_y_col.shape)
# print('partial',partial.shape)

#予測モデル
reg.fit(partial,f)

#回帰係数
print(pd.DataFrame({"Name":['f_t', 'f_x', 'f_y', 'f_xx', 'f_yy'],
                    "Coefficients":reg.coef_}).sort_values(by='Coefficients'))
print(reg.intercept_)

###Q.なぜちゃんと結果が出ないのか？
###A.座標が2次元のせいで初期値が2次元で存在してるのがうまくいかない理由？
###     それなら係数自体はどの座標点でとっても一定になるはず？
###  数値変化がちゃんと起きている点に対してのみ回帰分析をかけるべきかもしれない
###     変化なしはノイズデータなのか？邪魔にはなっていないのか？
###     そもそも変化なしの点が多くサンプルが足りていない可能性
###  方程式自体が不十分なのもありうる
###     微分項が足りてない可能性もある
###     xとyの２階微分を追加したらちょっとよくなった？
###Q.エクセルで一次元とはいえ複数点の場所を回帰分析してちゃんと結果が出ていたのはなぜか
###A.微分項しかないから定数部分が消去されて綺麗に見えていたとか？
