from eye_classifier.eyeClassifierModel import EyeClassifierModel
import numpy as np
import torch
from torchvision import transforms
from torch.autograd import Variable
from PIL import Image
import urllib.request
import os


class EyeClassifierInterface:
    def __init__(self, param_path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.create_model(param_path)
        self.classes = ['close', 'open']

    def create_model(self, param_path):
        model = EyeClassifierModel()
        model.load_state_dict(torch.load(param_path,  map_location=self.device))
        model = model.to(self.device)
        model.eval()
        return model

    def read_image(self, img_path):
        image = Image.open(img_path)
        if image.mode != "RGB":
            image = image.convert("RGB")
        return image
    
    @staticmethod
    def create(folder):
        param_path = os.path.join(folder, 'eye_classifier.pth')

        if not os.path.isdir(folder):
            print('Creating new folder to download params into')
            os.makedirs(folder)

        if not os.path.isfile(param_path) or not os.access(param_path, os.R_OK):
            print('Downloading parameters to path:', os.path.abspath(param_path))
            url = 'https://www.dropbox.com/s/phlrvrvjwe41ycc/eye_classifier_2.pth?dl=1'
            urllib.request.urlretrieve(url, param_path)
            print('Finished')

        return EyeClassifierInterface(param_path)

    
    # Take image input
    # Return a dictionary, which contains: 
    #   classes: ['close', 'open']
    #   label corresponding to classification result (0 for close and 1 for open)
    #   probability of belonging to each class
    def run(self, image):
        image_transforms = transforms.Compose([transforms.Resize(255),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),])
        image_tensor = image_transforms(image).float()
        image_tensor = image_tensor.unsqueeze_(0)
        input = Variable(image_tensor)
        input = input.to(self.device)
        output = self.model(input)
        output = torch.exp(output)
        output = torch.exp(output)
        index = output.data.cpu().numpy().argmax()

        result = {
            "classes": self.classes,
            "label": index,
            "probability": output.data.cpu().numpy()[0]
        }

        return result

if __name__=='__main__':
    img_path = 'open.jpg'
    interface = EyeClassifierInterface.create(folder='model_param')
    image = interface.read_image(img_path)
    res = interface.run(image)
    print(res)
