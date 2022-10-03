# Author: Filipe Chagas
# Email: filipe.ferraz0@gmail.com
# Github profile: github.com/FilipeChagasDev
# Description: Applies the "sepia" effect to an image using OpenCV and Numpy

import numpy as np
import cv2

def sepia(src_image):
    gray = cv2.cvtColor(src_image, cv2.COLOR_BGR2GRAY)
    normalized_gray = np.array(gray, np.float32)/255
    #solid color
    sepia = np.ones(src_image.shape)
    sepia[:,:,0] *= 153 #B
    sepia[:,:,1] *= 204 #G
    sepia[:,:,2] *= 255 #R
    #hadamard
    sepia[:,:,0] *= normalized_gray #B
    sepia[:,:,1] *= normalized_gray #G
    sepia[:,:,2] *= normalized_gray #R
    return np.array(sepia, np.uint8)
    
image = cv2.imread(raw_input('source filename: '))
image2 = sepia(image)
cv2.imshow('', image2)
cv2.waitKey()