import numpy as np
import json, codecs

filePath = './front/public/data.json'

with open(filePath, 'r') as readfile:
    data_json = json.load(readfile)
scalar_fields = np.array(data_json, np.float32)
print scalar_fields[0][0][0]
