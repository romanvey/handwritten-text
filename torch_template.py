from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch
import numpy as np
import os.path as osp
import os

class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        pass
        
    def forward(self, x):
        pass


class MyDataset(Dataset):
    def __init__(self):
        pass
        
    def __getitem__(self, idx):
        pass
    
    def __len__(self):
        pass


def accuracy(preds, y):
    rounded_preds = torch.argmax(preds)
    correct = (rounded_preds == y).float()
    acc = correct.sum() / len(correct)
    return acc

model_config = {
    'lr': 0.001
}

model = MyModel()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=model_config['lr'])

trainer_config = {
    'max_epochs': 20,
    'stop_steps': 2000,
    'every_steps': 400,
    'output_path': 'my_model'
}


training_set = MyDataset()
testing_set = MyDataset()

dataset_config = {
    'batch_size': 1,
    'shuffle': True,
    'num_workers': 2
}

train_laoder = DataLoader(training_set, **dataset_config)
test_loader = DataLoader(testing_set, **dataset_config)


def train(model, criterion, optimizer, train_loader, test_loader, device, trainer_config):
    max_epochs = trainer_config['max_epochs']
    stop_steps = trainer_config['stop_steps']
    every_steps = trainer_config['every_steps']
    output_path = trainer_config['output_path']
    best_metric = 0
    mode = 'max'


    for epoch in range(max_epochs):
        model.train()
        print("{} epoch starting!".format(epoch + 1))
        epoch_loss = 0
        epoch_acc = 0
        for step, (batch, labels) in enumerate(train_laoder):
            batch, labels = batch.to(device), labels.to(device).view(-1)
            optimizer.zero_grad()
            output = model(batch)
            loss = criterion(output, labels)
            
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
            if step % every_steps == 0:
                print("{} Iteration: loss - {}".format(step + 1, epoch_loss / (step + 1)))
            
            if step == stop_steps: 
                break
            
        print("Total epoch loss: {}".format(epoch_loss / (stop_steps + 1)))
        model.eval()
        with torch.set_grad_enabled(False):
            for step, (batch, labels) in enumerate(test_loader):
                batch, labels = batch.to(device), labels.to(device).view(-1)
                output = model(batch)
                acc = accuracy(output, labels)
                epoch_acc += acc.item()
                if step == stop_steps: 
                    break
        metric = epoch_acc / (stop_steps + 1)
        
        print("Epoch accuracy: {}".format())
        best_metric = save_model(model, metric, best_metric, mode, output_path)


def save_model(model, metric, best_metric, mode, output_path):
    to_save = osp.join('model_weights', output_path)
    os.makedirs(to_save, exist_ok=True)
    if mode == 'max':
        if metric >= best_metric:
            torch.save(model.state_dict(), osp.join(to_save, 'best.pth'))
            best_metric = metric
    elif mode == 'min':
        if metric <= best_metric:
            torch.save(model.state_dict(), osp.join(to_save, 'best.pth'))
            best_metric = metric
    else:
        print("Invalid mode! use 'max' or 'min'")
    torch.save(model.state_dict(), osp.join(to_save, 'last.pth'))
    return best_metric



def load_model(output_path, device, which='best.pth'):
    to_load = osp.join('model_weights', output_path, which)
    model = MyModel()
    model.load_state_dict(torch.load(to_load))
    model = model.to(device)
    model.eval()
    return model


if __name__ == '__main__':
    train(model, criterion, optimizer, train_loader, test_loader, device, trainer_config)