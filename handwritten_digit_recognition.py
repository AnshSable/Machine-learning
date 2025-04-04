

import torch
import torchvision
import torchvision.transforms as transforms

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,),(0.5,))
])

train_dataset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
test_dataset = torchvision.datasets.MNIST(root='./data', train=False, download=True, transform=transform)

train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=64, shuffle=True)
test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=64, shuffle=False)

import torch.nn as nn
import torch.nn.functional as F

class CNN(nn.Module):
  def __init__(self):
    super(CNN,self).__init__()

    self.conv1 = nn.Conv2d(in_channels =1 , out_channels = 6,kernel_size = 3)

    self.pool = nn.MaxPool2d(kernel_size=2,stride=2)

    self.conv2 = nn.Conv2d(in_channels=6,out_channels =16,kernel_size=3)

    self.fc1 = nn.Linear(16*5*5,120)
    self.fc2 = nn.Linear(120,84)
    self.fc3 = nn.Linear(84,10)

  def forward(self,x):
    x = self.pool(F.relu(self.conv1(x)))
    x = self.pool(F.relu(self.conv2(x)))
    x = x.view(-1,16*5*5)
    x = F.relu(self.fc1(x))
    x = F.relu(self.fc2(x))
    x=self.fc3(x)
    return x

model = CNN()

import torch.optim as optim

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(),lr=0.001)

epochs = 5

for epoch in range(epochs):
  running_loss =0.0

  for images,labels in train_loader:
    optimizer.zero_grad()

    outputs = model(images)
    loss = criterion(outputs,labels)

    loss.backward()
    optimizer.step()

    running_loss += loss.item()
  print(f"Epoch {epoch+1}, Loss: {running_loss / len(train_loader)}")

model.eval()

correct = 0
total = 0

with torch.no_grad():
  for images,labels in test_loader:
    outputs = model(images)
    _, predicted = torch.max(outputs,1)
    total += labels.size(0)
    correct +=(predicted==labels).sum().item()
accuracy = 100*correct/total
print(f"Model Accuracy on Test Data: {accuracy:.2f}%")

import torch
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import numpy as np


model.eval()

all_preds = []
all_labels=[]

with torch.no_grad():
  for images,labels in test_loader:
    outputs = model(images)  # Model ka output
    _, predicted = torch.max(outputs, 1)  # Max probability wala class lena
    all_preds.extend(predicted.cpu().numpy())  # Predictions store karna
    all_labels.extend(labels.cpu().numpy())  # Actual labels store karna

    cm= confusion_matrix(all_labels,all_preds)

    plt.figure(figsize=(8,6))
    sns.heatmap(cm,annot=True,fmt="d",cmap="Blues",xticklabels=np.arange(10),yticklabels=np.arange(10))
    plt.xlabel("predicted labels")
    plt.ylabel("actual labels")
    plt.title("confusion matrix")
    plt.show()

import torch
torch.save(model,"digit_model.pth")

