# -*- coding: utf-8 -*-

from PIL import Image
import cv2
import numpy as np
from matplotlib import pyplot as plt

#%%
    
def trySegmentation(zeroPadded, mask, img):
    minThresh = 25
    maxThresh = 56
    
    dst	= cv2.inRange(zeroPadded, minThresh, maxThresh)
    hemorrahage = (dst /255)* mask
    
    plt.imshow(hemorrahage, cmap = 'gray', interpolation = 'bicubic')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.xlabel('Automatic segmentation ')
    plt.show()
    
    plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.xlabel('Green channel')
    plt.show()
       
    
    choose = True
    while choose:
        
        election = str(input('Is the hemorrahage segmented good enough (yes/no): ')).upper()
            
        if election == 'YES':
            choose = False
        
        elif election == 'NO':
            histrH = cv2.calcHist([zeroPadded],[0], None,[256],[0,256])
            histrH[0] = 0
            plt.plot(histrH, color = 'g')
            plt.xlim([0,265])
            plt.grid(b=None, which='both', axis='both')
            plt.xlabel('Value [0, 255]')
            plt.ylabel('Frequency')
            plt.show()
            
            minThresh = int(input('The automatic threshold for min was {}, please choose another min value for thresholding: '.format(minThresh)))
            maxThresh = int(input('The automatic threshold for min was {}, please choose another min value for thresholding: '.format(maxThresh)))
            
            dst	= cv2.inRange(zeroPadded, minThresh, maxThresh)
            hemorrahage = (dst /255)* mask  
            
            plt.imshow(hemorrahage, cmap = 'gray', interpolation = 'bicubic')
            plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
            plt.xlabel('New segmentation')
            plt.show()
            
            plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
            plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
            plt.xlabel('Green channel')
            plt.show()
                        
        else: 
            print('Please write yes or no')
            election = str(input('Is the segmented optic disc almost the same as the original one (yes/no)')).upper()
    
    return(hemorrahage)




def segmentHemorrhage(image):
    myImage = image[:,:,1]
    
    _, mask = cv2.threshold(myImage,10,1,cv2.THRESH_BINARY)     
    gauBlur = cv2.GaussianBlur(src = myImage, ksize = (35, 35), sigmaX = 10, borderType = cv2.BORDER_DEFAULT)
    
    #Just ot check how good the blurr was done
    plt.imshow(gauBlur, cmap = 'gray', interpolation = 'bicubic')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.title('Gaus blurred segmentation')
    plt.show()
    
    #-----------------------------------------#
    zeroPadded = gauBlur* mask
    
    
    
    
    segmented = trySegmentation(zeroPadded, mask, myImage)
    
    return(segmented)
    
#%%


if __name__ == '__main__':    
    imageToRead = "path of the image"
    image = Image.open(imageToRead)
    img = np.asarray(image)
    hemorrhage = segmentHemorrhage(img)
    
    plt.imshow(hemorrhage, cmap = 'gray', interpolation = 'bicubic')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.title('Hemorrahge segmentation')
    plt.show()
    