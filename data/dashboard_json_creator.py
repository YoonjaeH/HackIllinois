import torch
from model import *
import pandas as pd
from helpers import *
from datetime import datetime
from constants import *
import json  
import torch
import numpy as np

data = pd.read_csv('./data/data_from_news.csv')
matrix, date_list = convert_data_to_matrix(data, group_data = True, group_days = 7)
x, actual = get_x_y(matrix, lookback = 4)
date_list = date_list[:x.shape[0]]

actual_dict = {d.strftime('%Y-%m-%d') : {} for d in date_list}

for i, date in enumerate(actual_dict.keys()):
    for j in range(US_NUM_STATES):
        state = US_STATE_NAMES[j].title()
        occ = int(actual[i, j])
        actual_dict[date].update({state: occ})

with open("./data/actual_data.json", "w") as outfile: 
    json.dump(actual_dict, outfile)

predict_dict = {d.strftime('%Y-%m-%d') : {} for d in date_list}
model = torch.load('./data/prediction_model.pt')
for i in range(len(x)):
    date = date_list[i].strftime('%Y-%m-%d')
    input_data = torch.from_numpy(x[i]).float().unsqueeze(0)
    output = model(input_data)
    pred = get_pred(output)
    for j in range(US_NUM_STATES):
        state = US_STATE_NAMES[j].title()
        occ = int(pred[0][j])
        predict_dict[date].update({state: occ})

with open("./data/predict_data.json", "w") as outfile: 
    json.dump(predict_dict, outfile)

max_dict = {d.strftime('%Y-%m-%d') : {} for d in date_list}

for i, date in enumerate(max_dict.keys()):
    cur_max = int(np.max(actual[i]))
    max_dict[date] = cur_max

with open("./data/max_data.json", "w") as outfile: 
    json.dump(max_dict, outfile)
