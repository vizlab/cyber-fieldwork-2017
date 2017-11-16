import numpy as np
import json, codecs
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
reg = linear_model.LinearRegression()

filePath = '../front/public/convection-diffusion.json'

with open(filePath, 'r') as readfile:
    data_json = json.load(readfile)
scalar_fields = np.array(data_json, np.float)

#標準化
def zscore(x, axis = None):
    xmean = x.mean(axis=axis, keepdims=True)
    xstd  = np.std(x, axis=axis, keepdims=True)
    zscore = (x-xmean)/xstd
    return zscore

#データ間の距離
dt = 0.0006250000000000001*10 #sec
dx = 0.1 #m
dy = 0.1 #m

#データの勾配
f_t = np.gradient(scalar_fields, axis=0)/dt
f_x = np.gradient(scalar_fields, axis=1)/dx
f_y = np.gradient(scalar_fields, axis=2)/dy
f_xx = np.gradient(f_x, axis=1)/dx
f_yy = np.gradient(f_y, axis=2)/dy

#回帰分析できる形に変形
f = scalar_fields.flatten()
f_t_col = f_t.flatten()
f_x_col = f_x.flatten()
f_y_col = f_y.flatten()
f_xx_col = f_xx.flatten()
f_yy_col = f_yy.flatten()
partial = np.c_[f_xx_col, f_yy_col, f, f_x_col, f_y_col]
partial = np.c_[f_xx_col, f_yy_col, f_y_col]

#回帰分析できる形に変形
# f = scalar_fields[:,40:60,50:60].flatten()
# f_t_col = f_t[:,40:60,50:60].flatten()
# f_x_col = f_x[:,40:60,50:60].flatten()
# f_y_col = f_y[:,40:60,50:60].flatten()
# f_xx_col = f_xx[:,40:60,50:60].flatten()
# f_yy_col = f_yy[:,40:60,50:60].flatten()
# partial = np.c_[f_xx_col, f_yy_col, f, f_x_col, f_y_col]
# partial = np.c_[f_xx_col, f_yy_col, f_y_col]

###変化のない部分と外れ値をdeleteする
partial = np.delete(partial, np.where(np.absolute(f_t_col)<1) ,0)
f_t_col = np.delete(f_t_col, np.where(np.absolute(f_t_col)<1))

plt.scatter(f_t_col,4*(partial[:,0]+partial[:,1])-10*partial[:,2]-f_t_col, s=1, c='purple', marker='s', label='Residual error')
plt.xlabel('f_t')
plt.ylabel('Residual error')
plt.savefig("../../test/reg_con_4.png")
plt.show()

partial = np.delete(partial, np.where(np.absolute(f_t_col)>1000) ,0)
f_t_col = np.delete(f_t_col, np.where(np.absolute(f_t_col)>1000))

#配列サイズ確認
# print('f',f.shape)
# print('f_t_col',f_t_col.shape)
# print('f_x_col',f_x_col.shape)
# print('f_y_col',f_y_col.shape)
# print('f_xx_col',f_xx_col.shape)
# print('f_yy_col',f_yy_col.shape)
# print('partial',partial.shape)

#標準化
# partial = zscore(partial, axis=0)
# f_t_col = zscore(f_t_col, axis=0)

print('f_t_col ave:',np.average(f_t_col))
print('|f_t_col| ave:',np.average(np.absolute(f_t_col)))

#予測モデル
reg.fit(partial,f_t_col)

#回帰係数
print(pd.DataFrame({"Name":['f_xx', 'f_yy','f_y'],# 'f', 'f_x', 'f_y'],
                    "Coefficients":reg.coef_}).sort_values(by='Coefficients'))
print("切片",reg.intercept_)
print("R2",reg.score(partial, f_t_col))

###残差プロット
X = reg.predict(partial)
plt.scatter(f_t_col, X - f_t_col, s=10, c='purple', marker='s', label='Residual error')
plt.hlines(y=0, xmin=-1000, xmax=1000, lw=2, color='red')
plt.xlabel('f_t')
plt.ylabel('Residual error')
plt.savefig("../../test/reg_con.png")
plt.show()
