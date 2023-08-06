import torch
import numpy as np
import torch.nn.functional as F
import urllib
import cv2
import os


class SmileCNN(torch.nn.Module):
  """
  A simple convolutional network.
  
  Map from inputs with shape [batch_size, 1, height, width] to
  outputs with shape [batch_size, 1].
  """
  
  def __init__(self):
    super().__init__()

    self.conv1 = torch.nn.Conv2d(1, 128, kernel_size=7, padding=7//2, stride=2)
    self.conv2 = torch.nn.Conv2d(128, 64, kernel_size=5, padding=5//2, stride=2)
    self.conv3 = torch.nn.Conv2d(64, 32, kernel_size=5, padding=5//2)
    self.conv4 = torch.nn.Conv2d(32, 16, kernel_size=3, padding=3//2)
    
    self.fully_connected1 = torch.nn.Conv2d(16, 8, kernel_size=1)
    self.fully_connected2 = torch.nn.Conv2d(8, 2, kernel_size=1)

  def forward(self, x):
    max_pool = torch.nn.MaxPool2d(2, 2)

    x = max_pool(F.relu(self.conv1(x)))
    x = max_pool(F.relu(self.conv2(x)))
    x = max_pool(F.relu(self.conv3(x)))
    x = max_pool(F.relu(self.conv4(x)))

    x = self.fully_connected1(x)
    x = F.relu(x)
    x = self.fully_connected2(x)
    x = x.squeeze(3)
    x = x.squeeze(2)
    return x

# takes in a grayscale image
def squarify(image):
    rows, cols = image.shape
    if rows > cols:
        # max y > max x; make cols match rows
        diff = rows - cols
        edge1 = diff // 2
        # if split is slightly uneven, adjust
        edge2 = edge1 + diff % 2
        return np.concatenate((np.zeros((rows, edge1), dtype='float'), image, np.zeros((rows, edge2), dtype='float')), axis=1)
        
    elif rows < cols:
        # max x > max y; make rows match cols
        diff = cols - rows
        edge1 = diff // 2
        # if split is slightly uneven, adjust
        edge2 = edge1 + diff % 2
        return np.concatenate((np.zeros((edge1, cols), dtype='float'), image, np.zeros((edge2, cols), dtype='float')))

    # if haven't returned yet, image is already square
    return image
    

OUTPUT_SIZE = 64

def standardize(image):
    mean = image.mean(keepdims=True)
    stdev = image.std(keepdims=True)
    
    image = squarify((image - mean) / stdev)
    # it's a square, so rows = cols
    rows, _ = image.shape
    scale = OUTPUT_SIZE / rows
    warp = np.array([
        [scale, 0, 0],
        [0, scale, 0]
    ])
    return cv2.warpAffine(image, warp, dsize=(OUTPUT_SIZE, OUTPUT_SIZE),
        borderMode=cv2.BORDER_CONSTANT, borderValue=0)


# input: an image of a single face
def is_smiling(image, folder=None):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    test_im = torch.from_numpy(np.float32(standardize(image)))[None, None, :, :]
    try:
        test_im = test_im.to(device)
        outputs = is_smiling.model(test_im)
    except AttributeError:
        # this is the first time we're running this, so initialize the neural network
        is_smiling.model = SmileCNN().to(device)
        is_smiling.model.float()

        if not os.path.isdir(folder):
            print('Creating new folder to download params into')
            os.makedirs(folder)

        param_path = os.path.join(folder, 'final_smile_net.pth')
        if not os.path.isfile(param_path) or not os.access(param_path, os.R_OK):
            print('Downloading parameters to path:', os.path.abspath(param_path))
            url = 'https://storage.googleapis.com/cv_final/model_dir/final_smile_net.pth'
            urllib.request.urlretrieve(url, param_path)
            print('Finished')

        is_smiling.model.load_state_dict(torch.load(param_path))
        outputs = is_smiling.model(test_im)
    
    soft = torch.nn.Softmax(1)
    return torch.max(outputs, 1)[1].item()
