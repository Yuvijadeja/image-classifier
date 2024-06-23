import joblib
import json
import cv2
import base64
import numpy as np
from wavelet import image_to_wavelet

__class_name_to_number = {}
__class_number_to_name = {}
__model = None

def loadSavedData():
    print("Loading Data...")
    global __model
    global __class_name_to_number
    global __class_number_to_name

    __model = joblib.load('./ml/image_classifier.joblib')

    with open('./ml/celebrity_names.json') as file:
        __class_name_to_number = json.load(file)
        __class_number_to_name = {v:k for k,v in __class_name_to_number.items()}
    print("Loaded Data...")

def base64_to_image(image_str: str):
    encoded_data = image_str.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def get_cropped_image(image_path, image):
    face_cascade = cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_eye.xml')

    if image_path:
        img = cv2.imread(image_path)
    else:
        img = base64_to_image(image)
    
    cropped_faces = []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            cropped_faces.append(roi_color)
    return cropped_faces
        
def classifier(image, image_path=None):
    images = get_cropped_image(image_path, image)

    results = []
    for image in images:
        scaled_image = cv2.resize(image, (32, 32))
        image_wave = image_to_wavelet(image, 'db1', 5)
        scaled_wave_image = cv2.resize(image_wave, (32, 32))
        combined_img = np.vstack((scaled_image.reshape(32*32*3, 1), scaled_wave_image.reshape(32*32, 1)))

        length_image_array = 32 * 32 * 3 + 32 * 32
        final = combined_img.reshape(1, length_image_array).astype(float)

        results.append({
            'name': __class_number_to_name[__model.predict(final)[0] - 1],
            'similarity': np.round(__model.predict_proba(final)*100, 2).tolist()[0],
            'celebrities': __class_name_to_number
        })
    return results

def test():
    with open('b64.txt') as file:
        return file.read()

if __name__ == '__main__':
    loadSavedData()
    # print(classifier(test(), None))
    # print(classifier(None, './test_images/virat3.jpg'))