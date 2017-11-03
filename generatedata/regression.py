import numpy as np
import json, codecs
import pandas as pd
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

f = scalar_fields.flatten()
f_t_col = f_t.flatten()
f_x_col = f_x.flatten()
f_y_col = f_y.flatten()
partial = np.c_[f_t_col, f_x_col, f_y_col]

print('f',f.shape)
print('f_t_col',f_t_col.shape)
print('f_x_col',f_x_col.shape)
print('f_y_col',f_y_col.shape)
print('partial',partial.shape)

#予測モデル
reg.fit(partial,f)

#回帰係数
print(pd.DataFrame({"Name":['f_t', 'f_x', 'f_y'],
                    "Coefficients":reg.coef_}).sort_values(by='Coefficients'))

print(reg.intercept_)

# gradient_fields = []
# t_grad_max_list = []
# x_grad_max_list = []
# y_grad_max_list = []
#
# for scalar_field in scalar_fields:
#     t_grad = np.gradient(scalar_fields, axis=0)
#     x_grad = np.gradient(scalar_fields, axis=1)
#     y_grad = np.gradient(scalar_fields, axis=2)
#
#     gradient_field = {
#         't': t_grad.tolist(),
#         'x': x_grad.tolist(),
#         'y': y_grad.tolist()
#     }
#
#     gradient_fields.append(gradient_field)
#     t_grad_max_list.append(t_grad.max())
#     x_grad_max_list.append(x_grad.max())
#     y_grad_max_list.append(y_grad.max())
