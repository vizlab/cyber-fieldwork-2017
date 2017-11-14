import numpy as np
import json, codecs

file_names = ['diffusion', 'convection-diffusion']

for file_name in file_names:
    file_path = './front/public/' + file_name + '.json'

    with open(file_path, 'r') as readfile:
        data_json = json.load(readfile)
    scalar_fields = np.array(data_json, np.float32)

    gradient_fields = []
    x_grad_max_list = []
    y_grad_max_list = []

    # calculate gradient fields
    for scalar_field in scalar_fields:
        x_grad = np.gradient(scalar_field, axis=0)
        y_grad = np.gradient(scalar_field, axis=1)
        gradient_field = {
            'x': x_grad.tolist(),
            'y': y_grad.tolist()
        }
        gradient_fields.append(gradient_field)
        x_grad_max_list.append(x_grad.max())
        y_grad_max_list.append(y_grad.max())

    file_path = './front/public/gradient-' + file_name + '.json'

    with open(file_path, 'w') as outfile:
        gradient_dict = {
            'data': gradient_fields,
            'x_grad_max': max(x_grad_max_list).tolist(),
            'y_grad_max': max(y_grad_max_list).tolist()
        }
        json.dump(gradient_dict, outfile)
