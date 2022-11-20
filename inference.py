

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from matplotlib import pyplot as plt
import scipy.stats

from get_info.get_odds import *
from get_info.http_boat_interactive import create_data


""" README
以下のものは自分で指定する必要があります．
    - 予想したいボートのパラメータ
    - ニューラルネットワークのモデルの指定
    - explanatory variableを学習と一致させる(全てのhotに対して合致している必要がある．)
"""

request_parameters = {'rno': '01', 'jcd': '02', 'hd': '20221119'}
net_1st = "net-weight/hot-1/2018_2022-9__2022_10_17_16_05_01" # 2018_2022-9"
net_2nd = "net-weight/hot-2/tmp" # 2018_2022-9"
net_3rd = "net-weight/hot-3/tmp"

cut_num_info = [3] # weather
player_cut_num_info = np.array( [7, 8, 13, 14, 16, 17, 20, 21, 22] )
inference_dict = create_data(request_parameters, 0)
inference_list = []
for value in inference_dict.values():
    inference_list.append(int( value ))
    

df = pd.DataFrame(inference_list)
df = df.T

def cut_info(func_cut_num_list: list, func_df=df) -> pd.DataFrame:
    print("avoiding curse of dimention")
    func_df = func_df.drop(columns=func_df.columns[func_cut_num_list])
    print(f"explanatory_size: {len(func_df.columns) - 6}")# -6: 被説明変数
    return func_df
for i in range(6):
    forEach_player = player_cut_num_info + (21 * i)
    cut_num_info.extend(list(forEach_player))
    
df = cut_info(cut_num_info)



# 説明変数と非説明変数の分離
x = df
x = scipy.stats.zscore(x, axis=1)
# pandas2numpy2torch.tensor
x = torch.tensor(x.values, dtype=torch.float32)

""""""
class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        x_size = len(cut_num_info) # x.size()[1]
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
        # x = self.softmax(x)
        return x
    
""""""
net_1st = torch.load(net_1st + ".pth")
net_1st.eval()
net_2nd = torch.load(net_2nd + ".pth")
net_2nd.eval()
net_3rd = torch.load(net_3rd + ".pth")
net_3rd.eval()

list_color = ["WHITE", "BLACK", "RED", "BLUE", "YELLOW", "GREEN"]


with torch.no_grad():
    probabilities_1st = net_1st(x)
    list_probabilities_1st = probabilities_1st.tolist()[0]
    probabilities_2nd = net_2nd(x)
    list_probabilities_2nd = probabilities_2nd.tolist()[0]
    probabilities_3rd = net_3rd(x)
    list_probabilities_3rd = probabilities_3rd.tolist()[0]
    first_place = list_color[list_probabilities_1st.index(max(list_probabilities_1st))]
    second_place = list_color[list_probabilities_2nd.index(max(list_probabilities_2nd))]
    third_place = list_color[list_probabilities_3rd.index(max(list_probabilities_3rd))]
    print(f"{list_probabilities_1st}\n{list_probabilities_2nd}\n{list_probabilities_3rd}")
    print(f"{first_place}\n{second_place}\n{third_place}")