import numpy as np
import json

filePath = './front/public/data.json'

with open(filePath, 'r') as readfile:
    data_json = json.load(readfile)
scalar_fields = np.array(data_json, np.float32)

f_t = np.gradient(scalar_fields, axis=0)
f_x = np.gradient(scalar_fields, axis=1)
f_y = np.gradient(scalar_fields, axis=2)
f_tt = np.gradient(f_t, axis=0)
f_xx = np.gradient(f_x, axis=1)
f_yy = np.gradient(f_y, axis=2)

filePath = './ccm/difference-data.json'

with open(filePath, 'w') as outfile:
    difference_dict = {
        'f': scalar_fields.tolist(),
        'f_t': f_t.tolist(),
        'f_x': f_x.tolist(),
        'f_y': f_y.tolist(),
        'f_tt': f_tt.tolist(),
        'f_xx': f_xx.tolist(),
        'f_yy': f_yy.tolist()
    }
    json.dump(difference_dict, outfile)
