#read image located in data/1_14_1.jpg
import cv2
import numpy as np

img = cv2.imread('data/1_14_Imagen2.png')
#count values in image
print(img[0])
unique, counts = np.unique(img[0].flatten(), return_counts=True)
print(np.unique(img[0], return_counts=True))
print('----')
print(np.unique(img[1], return_counts=True))
print('----')
print(np.unique(img[2], return_counts=True))
#test image in test/
