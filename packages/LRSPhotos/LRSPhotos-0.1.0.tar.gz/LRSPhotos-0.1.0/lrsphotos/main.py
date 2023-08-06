import cv2
import numpy as np
import  matplotlib.pyplot as plt

from face_detector.interface import FaceDetectorInterface
from smile_classifier.interface import is_smiling
from eye_detector.interface import EyeDetectorInterface
from eye_classifier.interface import EyeClassifierInterface

from PIL import Image


def draw(results, image):
    font_scale = 0.5
    thickness = 1
    for face_res in results:
        cv2.rectangle(image, face_res['face_start'], face_res['face_end'], (0, 255, 0), 2)
        smiling_status = 'smiling' if face_res['smiling'] else 'not smiling'
        cv2.putText(image, smiling_status, face_res['face_start'],
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0),
                    thickness, cv2.LINE_AA)

        if face_res['eye1_start'] and face_res['eye1_end']:
            cv2.rectangle(image, face_res['eye1_start'], face_res['eye1_end'], (0, 255, 0), 2)
            eye_status = 'open' if face_res['eye1_open'] else 'closed'
            cv2.putText(image, eye_status, face_res['eye1_start'],
                        cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0),
                        thickness, cv2.LINE_AA)

        if face_res['eye2_start'] and face_res['eye2_end']:
            cv2.rectangle(image, face_res['eye2_start'], face_res['eye2_end'], (0, 255, 0), 2)
            eye_status = 'open' if face_res['eye2_open'] else 'closed'
            cv2.putText(image, eye_status, face_res['eye2_start'],
                        cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0),
                        thickness, cv2.LINE_AA)

    return image


def run(img=None, image_path=None, data_folder='model_data'):
    final_results = []

    if image_path:
        img = np.array(Image.open(image_path))

    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    face_detector = FaceDetectorInterface.create(data_folder)
    eye_detector = EyeDetectorInterface.create(data_folder)
    eye_classifier = EyeClassifierInterface.create(data_folder)

    res = face_detector.run(img)
    for result in res:
        one_face_results = {
            'face_start': (result['x1'], result['y1']),
            'face_end': (result['x2'], result['y2']),
            'eye1_start': None,
            'eye1_end': None,
            'eye2_start': None,
            'eye2_end': None,
            'smiling': None,
            'eye1_open': None,
            'eye2_open': None
        }

        x1 = result['x1']
        x2 = result['x2']
        y1 = result['y1']
        y2 = result['y2']

        # extract the actual face image from the box coordinates
        face = cv2.getRectSubPix(gray_img,
                                 (x2 - x1, y2 - y1),
                                 ((x2 + x1) / 2, (y2 + y1) / 2))

        color_face = cv2.getRectSubPix(cv2.cvtColor(img, cv2.COLOR_RGBA2RGB),
                                        (x2 - x1, y2 - y1),
                                        ((x2 + x1) / 2, (y2 + y1) / 2))

        # TODO: fix
        one_face_results['smiling'] = True

        try:
            eyes, radius = eye_detector.detect(face)
            eye1, eye2 = eyes
            diameter = 2 * radius
        except:
            continue

        # Drawing eyes on image
        for i, eye in enumerate([eye1, eye2]):
            start = eye[0] - radius + x1, eye[1] - radius + y1
            end = eye[0] + radius + x1, eye[1] + radius + y1
            one_face_results['eye%d_start' % (i+1)] = start
            one_face_results['eye%d_end' % (i+1)] = end

        eye1 = cv2.getRectSubPix(color_face, (diameter, diameter), tuple(eye1))
        eye2 = cv2.getRectSubPix(color_face, (diameter, diameter), tuple(eye2))

        eye1_result = eye_classifier.run(Image.fromarray(eye1))['label']
        eye2_result = eye_classifier.run(Image.fromarray(eye2))['label']

        one_face_results['eye1_open'] = True if eye1_result == 1 else False
        one_face_results['eye2_open'] = True if eye2_result == 1 else False

        final_results.append(one_face_results)

    return final_results


if __name__ == '__main__':
    image_path = '../face_detector/input_images/family.jpeg'
    img = np.array(Image.open(image_path))
    res = run(img)
    image = draw(res, img)
    plt.imshow(image)
    plt.show()