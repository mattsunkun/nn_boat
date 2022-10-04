from pickle import TRUE
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from matplotlib import pyplot as plt
import scipy.stats

test_name = "1_hot_vector_2022" # "1_hot_vector_20200101_20220923"
name_net = "net_weight_1_hot_vector_2021.pth"
df = pd.read_csv("http_csv/" + test_name + ".csv", header=None)

# 説明変数と非説明変数の分離
x = df.drop(df.columns[-6:], axis=1)
x = scipy.stats.zscore(x)
t = df.drop(df.columns[:-6], axis=1)

# pandas2numpy2torch.tensor
x = torch.tensor(x.values, dtype=torch.float32)
t = torch.tensor(t.values, dtype=torch.float32)

# xとtの合成
dataset = torch.utils.data.TensorDataset(x, t)

# データの使用目的による分割
torch.manual_seed(0)
n_train = int( len( dataset ) * 0.5 )
n_test = int( len( dataset ) - n_train)
train, test = torch.utils.data.random_split(dataset, [n_train, n_test])
      
# shuffle はデフォルトで False のため、学習データのみ True に指定
batch_size = 10
train_loader = torch.utils.data.DataLoader(train, batch_size, shuffle=True)
test_loader = torch.utils.data.DataLoader(test, batch_size)

# nnのモデル定義
# 一位を予想するときは132->6
class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        x_size = x.size()[1]
        t_size = t.size()[1]
        k = 100
        self.fc1 = nn.Linear(x_size, k)
        self.fc2 = nn.Linear(k, k)
        self.fc3 = nn.Linear(k, t_size)
        self.relu = nn.SiLU()
        self.norm = nn.BatchNorm1d(k)
        
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.norm(x)
        for i in range(0):
            x = self.fc2(x)
            x = self.relu(x)
            x = self.norm(x)
        x = self.fc3(x)
        x = nn.Softmax(dim=1)(x)
        return x

# 本番はここから
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print( f"device: {device}" )

max_epoch = 100
net = torch.load(name_net).to(device)
optimizer = torch.optim.Adam(net.parameters())
criterion = F.cross_entropy

test_loss_list = []
test_accuracy_list = []
with torch.no_grad():
    for epoch in range(max_epoch):
        running_loss = 0.0
        test_accuracy = 0.0
        for batch in test_loader:
            explanatory_variables, answer_label = batch
            explanatory_variables = explanatory_variables.to(device)
            answer_label = answer_label.to(device)
            
            predict_label = net(explanatory_variables)
            loss = criterion(predict_label, answer_label)
            
            running_loss += loss.item()
            
            predict_nth = predict_label.data.max(1)[1] #予測結果
            answer_nth = torch.argmax(t)
            test_accuracy += torch.sum(predict_nth == answer_nth).item()

            
        test_loss_list.append(running_loss)
        test_accuracy_list.append(test_accuracy/n_test)
print("test loss")
print(test_loss_list[-1])
fig, ax = plt.subplots(ncols=1, nrows=2, facecolor="lightgray")
ax[0].set_title("lost")
ax[0].plot(test_loss_list) 
ax[1].set_title("prob")
ax[1].plot(test_accuracy_list) 
plt.show()