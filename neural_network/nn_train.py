import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import scipy.stats
import time
import torch
import torch.nn as nn
import torch.nn.functional as F

# from nn_model import Net

before_preprocessing = time.time()

train_name = "hot-1/2018_2022-9"# "hot-1/20200101_20220923" 
df = pd.read_csv("train-data/" + train_name + ".csv", header=None)
name_net = "net-weight/" + train_name + ".pth"
name_fig = "net-weight/" + train_name + ".png"
net_bool = True


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
test_loader = torch.utils.data.DataLoader(test, n_test, shuffle=True)

######

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
    
#######
# 本番はここから
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print( f"device: {device}" )

max_epoch = 100
net = Net().to(device)
optimizer = torch.optim.Adam(net.parameters())
criterion = F.cross_entropy

after_preprocessing = time.time()
print(f"preprocessing time: {after_preprocessing - before_preprocessing}")
before_training = time.time()

train_loss_list = []
train_accuracy_list = []
for epoch in range(max_epoch):
    running_loss = 0.0
    train_accuracy = 0.0
    for batch in train_loader:
        explanatory_variables, answer_label = batch
        explanatory_variables = explanatory_variables.to(device)
        answer_label = answer_label.to(device)
        
        optimizer.zero_grad()
        predict_label = net(explanatory_variables)
        loss = criterion(predict_label, answer_label)
        
        running_loss += loss.item()
        
        loss.backward()
        optimizer.step()
        
        # predict_nth = predict_label.data.max(1)[1] #予測結果
        predict_nth = predict_label.argmax(1)
        # answer_nth = torch.argmax(answer_label)
        answer_nth = answer_label.argmax(1)
        """
        print(predict_label)
        print(answer_label)
        print(predict_nth)
        print(answer_nth)
        print((predict_nth == answer_nth).sum().item())
        """
        # train_accuracy += torch.sum(predict_nth == answer_nth).item()
        train_accuracy += (predict_nth == answer_nth).sum().item()

        
    train_loss_list.append(running_loss)
    train_accuracy_list.append(train_accuracy/n_train)

after_training = time.time()
print(f"training time: {after_training - before_training}")
before_testing = time.time()

test_accuracy = 0.0
with torch.no_grad():
    for batch in test_loader:
        explanatory_variables, answer_label = batch
        explanatory_variables = explanatory_variables.to(device)
        answer_label = answer_label.to(device)
        
        predict_label = net(explanatory_variables)
        loss = criterion(predict_label, answer_label)
        
        predict_nth = predict_label.data.max(1)[1] #予測結果
        answer_nth = torch.argmax(answer_label)
        test_accuracy += torch.sum(predict_nth == answer_nth).item()


test_accuracy /= n_test

after_testing = time.time()
print(f"testing time: {after_testing - before_testing}")
   
if net_bool: 
    print(f"save model as: {name_net}")
    torch.save(net, name_net)

print(f"train loss: {train_loss_list[-1]}")
print(f"test accuracy: {test_accuracy}")
fig, ax = plt.subplots(ncols=1, nrows=2, facecolor="lightgray")

plt.subplots_adjust(hspace=0.4)
ax[0].set_title(f"train loss ( train time: {after_training - before_training} )")
ax[0].plot(train_loss_list) 
ax[1].set_title(f"train prob ( test prob: {test_accuracy} )")
ax[1].plot(train_accuracy_list) 
plt.savefig(name_fig)
plt.show()