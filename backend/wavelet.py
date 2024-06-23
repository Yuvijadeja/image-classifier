import pywt
import numpy as np
import cv2

def image_to_wavelet(img, mode='haar', level=1):
    imArray = img
    imArray = cv2.cvtColor(imArray, cv2.COLOR_RGB2GRAY)
    imArray = np.float32(imArray)
    imArray /= 255
    coeffs = pywt.wavedec2(imArray, mode, level=level)
    coeffsH = list(coeffs)
    coeffsH[0] *= 0;
    imArrayH = pywt.waverec2(coeffsH, mode)
    imArrayH *= 255
    imArrayH = np.uint8(imArrayH)
    return imArrayH