from interface import EyeClassifierInterface


if __name__ == "__main__":
    img_path = 'open.jpg'
    
    folder = './'
    eye_classifier = EyeClassifierInterface.create(folder=folder)
    image = eye_classifier.read_image(img_path)
    res = eye_classifier.run(image)
    print(res)
