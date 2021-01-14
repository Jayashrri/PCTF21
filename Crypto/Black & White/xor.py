import cv2  
import numpy as np  
     
# path to input images are specified and   
# images are loaded with imread command  
img1 = cv2.imread('full_b.png')  
img2 = cv2.imread('flip_b.png') 
  
# cv2.bitwise_xor is applied over the 
# image inputs with applied parameters  
dest_xor = cv2.bitwise_xor(img1, img2, mask = None) 
  
# the window showing output image 
# with the Bitwise XOR operation 
# on the input images 
cv2.imwrite('test_b.png', dest_xor)  