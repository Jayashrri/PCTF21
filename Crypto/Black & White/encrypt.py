from stegano import lsb
#secret = lsb.hide("center.png", "Hello World")
#secret.save("secret.png")

import cv2 
import numpy as np 
import random 
 
def encrypt(): 
      
    # img1 and img2 are the 
    # two input images 
    img1 = cv2.imread('hello.png') 
    img2 = cv2.imread('qr_c.png') 
      
    for i in range(img2.shape[0]): 
        for j in range(img2.shape[1]): 
            for l in range(3): 
                  
                # v1 and v2 are 8-bit pixel values 
                # of img1 and img2 respectively 
                v1 = format(img1[i][j][l], '08b') 
                v2 = format(img2[i][j][l], '08b') 
                  
                # Taking 4 MSBs of each image 
                v3 = v1[:4] + v2[:4]  
                  
                img1[i][j][l]= int(v3, 10) 
                  
    cv2.imwrite('pt.png', img1) 
	
encrypt()