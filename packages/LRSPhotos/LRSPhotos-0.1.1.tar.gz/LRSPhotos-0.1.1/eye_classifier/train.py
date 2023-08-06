from eyeClassifierModel import EyeClassifierModel
import numpy as np
import torch
from torch import nn
from torch import optim
from torchvision import datasets, transforms, models
from torch.utils.data import Dataset, DataLoader
from torch.utils.data.sampler import SubsetRandomSampler

def load_split_train_test(datadir, trans, test_size = .2, batch=64):
    data = datasets.ImageFolder(datadir,transform=trans)
    num_data = len(data)
    print(num_data)
    indices = list(range(num_data))
    split = int(np.floor(test_size * num_data))
    np.random.shuffle(indices)
    train_idx, test_idx = indices[split:], indices[:split]
    train_sampler = SubsetRandomSampler(train_idx)
    test_sampler = SubsetRandomSampler(test_idx)
    trainloader = torch.utils.data.DataLoader(data, sampler=train_sampler, batch_size=batch, num_workers=4)
    testloader = torch.utils.data.DataLoader(data, sampler=test_sampler, batch_size=batch, num_workers=4)
    return trainloader, testloader

# Data Normalization
def data_normalizer():
    return transforms.Compose([transforms.Resize(255),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),])

if __name__ == '__main__':
    BATCH_SIZE=64
    data_dir = "./data/classified_data/"

    trans = data_normalizer()
    train_loader, val_loader = load_split_train_test(data_dir, trans, .2, BATCH_SIZE)

    model = EyeClassifierModel()
    model.load_state_dict(torch.load('eye_classifier.pth'))

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    criterion = nn.NLLLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    epochs = 5
    for epoch in range(epochs):
        train_loss = 0
        val_loss = 0
        accuracy = 0

        model.train()
        counter = 0
        for inputs, labels in train_loader:
            # Move to device
            inputs, labels = inputs.to(device), labels.to(device)
            # Clear optimizers
            optimizer.zero_grad()
            # Forward pass
            output = model.forward(inputs)
            # Loss
            loss = criterion(output, labels)
            # Calculate gradients (backpropogation)
            loss.backward()
            # Adjust parameters based on gradients
            optimizer.step()
            # Add the loss to the training set's rnning loss
            train_loss += loss.item()*inputs.size(0)
            
            # Print the progress of our training
            counter += 1
            if counter % 10 == 0:
                print(counter, "/", len(train_loader))
            
        # Evaluating the model
        model.eval()
        counter = 0
        # Tell torch not to calculate gradients
        with torch.no_grad():
            for inputs, labels in val_loader:
                # Move to device
                inputs, labels = inputs.to(device), labels.to(device)
                # Forward pass
                output = model.forward(inputs)
                # Calculate Loss
                valloss = criterion(output, labels)
                # Add loss to the validation set's running loss
                val_loss += valloss.item()*inputs.size(0)
                
                # Since our model outputs a LogSoftmax, find the real 
                # percentages by reversing the log function
                # output = torch.exp(output)
                # Get the top class of the output
                top_p, top_class = output.topk(1, dim=1)
                # See how many of the classes were correct?
                equals = top_class == labels.view(*top_class.shape)
                # Calculate the mean (get the accuracy for this batch)
                # and add it to the running accuracy for this epoch
                accuracy += torch.mean(equals.type(torch.FloatTensor)).item()

                
                # Print the progress of our evaluation
                counter += 1
                if (counter % 10 == 0):
                    print(counter, "/", len(val_loader))
        
        # Get the average loss for the entire epoch
        train_loss = train_loss/len(train_loader.dataset)
        valid_loss = val_loss/len(val_loader.dataset)
        # Print out the information
        print('Accuracy: ', accuracy/len(val_loader))
        print('Epoch: {} \tTraining Loss: {:.6f} \tValidation Loss: {:.6f}'.format(epoch, train_loss, valid_loss))

    # Save the model after training
    torch.save(model.state_dict(), 'eye_classifier_more_training.pth')