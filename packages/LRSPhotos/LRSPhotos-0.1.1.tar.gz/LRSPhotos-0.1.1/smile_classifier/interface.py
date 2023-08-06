import torch
import numpy as np
import torch.nn.functional as F
import cv2

PATH = 'smile_classifier/smile_net_with_max_pooling_9.pth'


class SmileCNN(torch.nn.Module):
  """
  A simple convolutional network.
  
  Map from inputs with shape [batch_size, 1, height, width] to
  outputs with shape [batch_size, 1].
  """
  
  def __init__(self):
    super().__init__()
#    self.conv1 = torch.nn.Conv2d(1, 128, kernel_size=7, padding=7//2) # feel free to change these parameters.
#    self.conv2 = torch.nn.Conv2d(128, 64, kernel_size=7, padding=7//2, stride=4)
#    self.conv3 = torch.nn.Conv2d(64, 32, kernel_size=7, padding=7//2, stride=2)
#    self.conv4 = torch.nn.Conv2d(32, 32, kernel_size=7, padding=7//2, stride=2)
    
    self.conv1 = torch.nn.Conv2d(1, 64, kernel_size=7, padding=7//2) # feel free to change these parameters.
    self.conv2 = torch.nn.Conv2d(64, 48, kernel_size=7, padding=7//2, stride=2)
    self.conv3 = torch.nn.Conv2d(48, 32, kernel_size=7, padding=7//2, stride=2)
    self.conv4 = torch.nn.Conv2d(32, 32, kernel_size=7, padding=7//2, stride=2)
    
    self.conv_final = torch.nn.Conv2d(32, 2, kernel_size=1)
    
  def forward(self, x):
    pool = torch.nn.MaxPool2d(2, 2)
    x = pool(F.relu(self.conv1(x)))
    x = pool(F.relu(self.conv2(x)))
    x = pool(F.relu(self.conv3(x)))
    x = F.relu(self.conv4(x))
    x = self.conv_final(x)
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
        return np.concatenate((np.zeros((rows, edge1), dtype='float'), image, \
                               np.zeros((rows, edge2), dtype='float')), axis=1)
    elif rows < cols:
        # max x > max y; make rows match cols
        diff = cols - rows
        edge1 = diff // 2
        # if split is slightly uneven, adjust
        edge2 = edge1 + diff % 2
        return np.concatenate((np.zeros((edge1, cols), dtype='float'), image, \
                               np.zeros((edge2, cols), dtype='float')))

    # if haven't returned yet, image is already square
    return image
    

OUTPUT_SIZE = 64

def standardize(image):
    image = squarify(image)
    # it's a square, so rows = cols
    rows, _ = image.shape
    scale = OUTPUT_SIZE / rows
    warp = np.array([
        [scale, 0, 0],
        [0, scale, 0],
        [0, 0, 1]
    ])
    return cv2.warpPerspective(image, warp, dsize=(OUTPUT_SIZE, OUTPUT_SIZE),
        borderMode=cv2.BORDER_REPLICATE)


# input: an image of a single face
def is_smiling(image):
    test_im = torch.from_numpy(np.float32(standardize(image)))[None, None, :, :]
    try:
        outputs = is_smiling.model(test_im)
    except AttributeError:
        # this is the first time we're running this, so initialize the neural network
        is_smiling.model = SmileCNN()
        is_smiling.model.float()
        # use CUDA if we have it
        if torch.cuda.is_available():
            is_smiling.model.cuda()
        
        is_smiling.model.load_state_dict(torch.load(PATH))
        
        # rerun the code that failed
        outputs = is_smiling.model(test_im)
        
    cv2.imwrite("smile_face.png", np.float32(standardize(image)))
        
    return torch.max(outputs, 1)[1].item()
