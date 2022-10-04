

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from matplotlib import pyplot as plt
import scipy.stats

from get_info.get_odds import *
from get_info.http_boat import create_data
# from get_player_info.hot_vector import hot_vector_nth_list
# from neural_network.nn_model import Net


"""
    request_parameters: 
    nth_pth_name: 
"""

request_parameters = {'rno': '01', 'jcd': '01', 'hd': '20220102'}
net_1st = "net-weight/hot-1/tmp" # 2018_2022-9"
net_2nd = "net-weight/hot-2/tmp" # 2018_2022-9"
net_3rd = "net-weight/hot-3/tmp"
inference_dict = create_data(request_parameters, 0)
# inference_dict = {'air_temperature': 200, 'weather': 1, 'wind_speed': 3, 'wind_direction': 1, 'water_temperature': 230, 'wave_height': 2, '1_rank': 3, '1_age': 46, '1_weight*10': 470, '1_F': 0, '1_L': 0, '1_avg_st*100': 19, '1_jp_first': 433, '1_jp_second': 2500, '1_jp_third': 4423, '1_local_first': 357, '1_local_second': 1429, '1_local_third': 2857, '1_motor_second': 4194, '1_motor_third': 6237, '1_boat_second': 4229, '1_boat_third': 5829, '1_display_time': 687, '1_tilt': -5, '1_steal_place': 1, '1_fsl_timing': -1, '1_display_start_timing': 6, '2_rank': 1, '2_age': 34, '2_weight*10': 481, '2_F': 0, '2_L': 0, '2_avg_st*100': 17, '2_jp_first': 625, '2_jp_second': 4808, '2_jp_third': 6346, '2_local_first': 610, '2_local_second': 4694, '2_local_third': 6327, '2_motor_second': 3656, '2_motor_third': 5215, '2_boat_second': 3963, '2_boat_third': 5427, '2_display_time': 684, '2_tilt': -5, '2_steal_place': 2, '2_fsl_timing': 0, '2_display_start_timing': 24, '3_rank': 2, '3_age': 58, '3_weight*10': 484, '3_F': 0, '3_L': 0, '3_avg_st*100': 23, '3_jp_first': 444, '3_jp_second': 1800, '3_jp_third': 3600, '3_local_first': 344, '3_local_second': 370, '3_local_third': 2222, '3_motor_second': 3962, '3_motor_third': 4906, '3_boat_second': 3989, '3_boat_third': 5899, '3_display_time': 685, '3_tilt': -5, '3_steal_place': 3, '3_fsl_timing': 0, '3_display_start_timing': 25, '4_rank': 2, '4_age': 35, '4_weight*10': 465, '4_F': 0, '4_L': 0, '4_avg_st*100': 17, '4_jp_first': 497, '4_jp_second': 2667, '4_jp_third': 5111, '4_local_first': 476, '4_local_second': 2778, '4_local_third': 5000, '4_motor_second': 3134, '4_motor_third': 4700, '4_boat_second': 3333, '4_boat_third': 5172, '4_display_time': 697, '4_tilt': 0, '4_steal_place': 4, '4_fsl_timing': 0, '4_display_start_timing': 9, '5_rank': 2, '5_age': 21, '5_weight*10': 445, '5_F': 1, '5_L': 0, '5_avg_st*100': 16, '5_jp_first': 394, '5_jp_second': 1977, '5_jp_third': 2907, '5_local_first': 394, '5_local_second': 1667, '5_local_third': 2963, '5_motor_second': 3682, '5_motor_third': 5124, '5_boat_second': 3111, '5_boat_third': 4611, '5_display_time': 683, '5_tilt': -5, '5_steal_place': 5, '5_fsl_timing': 0, '5_display_start_timing': 4, '6_rank': 3, '6_age': 23, '6_weight*10': 450, '6_F': 1, '6_L': 0, '6_avg_st*100': 19, '6_jp_first': 151, '6_jp_second': 0, '6_jp_third': 213, '6_local_first': 138, '6_local_second': 238, '6_local_third': 238, '6_motor_second': 4845, '6_motor_third': 6584, '6_boat_second': 3923, '6_boat_third': 5691, '6_display_time': 686, '6_tilt': -5, '6_steal_place': 6, '6_fsl_timing': 0, '6_display_start_timing': 18} # , 'order_1': 2, 'order_2': 3, 'order_3': 5}
inference_list = []
for value in inference_dict.values():
    inference_list.append(int( value ))
    

df = pd.DataFrame(inference_list)
df = df.T
# 説明変数と非説明変数の分離
x = df
x = scipy.stats.zscore(x, axis=1)
# pandas2numpy2torch.tensor
x = torch.tensor(x.values, dtype=torch.float32)

""""""
class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        x_size = 132 # x.size()[1]
        t_size = 6 # t.size()[1]
        k = 100
        self.fc1 = nn.Linear(x_size, k)
        self.fc2 = nn.Linear(k, k)
        self.fc3 = nn.Linear(k, t_size)
        self.relu = nn.SiLU()
        self.norm = nn.BatchNorm1d(k)
        self.softmax = nn.Softmax(dim=1)
        
        
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.norm(x)
        for i in range(3):
            x = self.fc2(x)
            x = self.relu(x)
            x = self.norm(x)
        x = self.fc3(x)
        x = self.softmax(x)
        return x
    
""""""
net_1st = torch.load(net_1st + ".pth")
net_2nd = torch.load(net_2nd + ".pth")
net_3rd = torch.load(net_3rd + ".pth")

list_color = ["WHITE", "BLACK", "RED", "BLUE", "YELLOW", "GREEN"]
net_1st.eval()
net_2nd.eval()
net_3rd.eval()

with torch.no_grad():
    probabilities_1st = net_1st(x)
    list_probabilities_1st = probabilities_1st.tolist()[0]
    probabilities_2nd = net_2nd(x)
    list_probabilities_2nd = probabilities_2nd.tolist()[0]
    probabilities_3rd = net_3rd(x)
    list_probabilities_3rd = probabilities_3rd.tolist()[0]
    print(f"{list_probabilities_1st}\n{list_probabilities_2nd}\n{list_probabilities_3rd}")
    first_place = list_color[list_probabilities_1st.index(max(list_probabilities_1st))]
    second_place = list_color[list_probabilities_2nd.index(max(list_probabilities_2nd))]
    third_place = list_color[list_probabilities_3rd.index(max(list_probabilities_3rd))]
    print(f"{first_place}\n{second_place}\n{third_place}")