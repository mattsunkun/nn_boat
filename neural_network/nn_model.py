import torch
import torch.nn as nn
import torch.nn.functional as F

# nnのモデル定義
# 一位を予想するときは132->6

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