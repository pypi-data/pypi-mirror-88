from eyeClassifierModel import EyeClassifierModel
import numpy as np
import torch
from torch import nn
from torch import optim
from torchvision import datasets, transforms, models
from torch.utils.data import Dataset, DataLoader
from torch.utils.data.sampler import SubsetRandomSampler

def load_test_data(datadir, trans, test_size = .2, batch=64):
    data = datasets.ImageFolder(datadir,transform=trans)
    dataloader = torch.utils.data.DataLoader(data, batch_size=batch, num_workers=4)
    return dataloader

# Data Normalization
def data_normalizer():
    return transforms.Compose([transforms.Resize(255),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),])

if __name__ == '__main__':
    BATCH_SIZE=64
    data_dir = "./data/test_data/"

    trans = data_normalizer()
    dataloader = load_test_data(data_dir, trans, BATCH_SIZE)

    model = EyeClassifierModel()
    model.load_state_dict(torch.load('eye_classifier.pth'))
    model.eval()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    criterion = nn.NLLLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    loss = 0
    corrects = 0.0

    i = 0

    print(len(dataloader.dataset))

    for inputs, labels in dataloader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model(inputs)
        loss = criterion(outputs, labels)

        _, preds = torch.max(outputs, 1)

        loss += loss.item() * inputs.size(0)
        corrects += torch.sum(preds == labels.data)
        print(corrects)

        i += 1

    final_loss = loss / len(dataloader.dataset)
    final_acc = corrects.double() / len(dataloader.dataset)
    
    print('Loss: {:.4f} Acc: {:.4f}'.format(final_loss, final_acc))