import numpy as np
import json, codecs

filePath = './front/public/data.json'

with open(filePath, 'r') as readfile:
    data_json = json.load(readfile)
scalar_fields = np.array(data_json, np.float32)

gradient_fields = []
for scalar_field in scalar_fields:
    gradient_field = {
        'x': np.gradient(scalar_field, axis=1).tolist(),
        'y': np.gradient(scalar_field, axis=0).tolist()
    }
    gradient_fields.append(gradient_field)


filePath = './front/public/gradient-fields.json'
with open(filePath, 'w') as outfile:
    gradient_dict = {
        'data': gradient_fields
    }
    json.dump(gradient_dict, outfile)

