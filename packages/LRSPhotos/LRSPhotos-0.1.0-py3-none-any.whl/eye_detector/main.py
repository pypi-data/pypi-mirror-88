#!/usr/bin/env python3
from interface import EyeDetectorInterface
import cv2

if __name__ == "__main__":
    img = cv2.imread('../face_detector/input_images/small_img.png', cv2.IMREAD_GRAYSCALE)

    try:
        interface = EyeDetectorInterface()
        eye1, eye2, length = interface.detect(img) # img is the face image FaceDetector outputs
        print(eye1, eye2, length)
    except:
        print("Eyes not detected!")

    # my outputs for eye classification
    eye1_img = img[(eye1[0]-length):(eye1[0]+length), (eye1[1]-length):(eye1[1]+length)]
    eye2_img = img[(eye2[0]-length):(eye2[0]+length), (eye2[1]-length):(eye2[1]+length)]

    


    
