# -*- coding: utf-8 -*-

from PIL import Image
import cv2
import numpy as np
from matplotlib import pyplot as plt



#%%
# STEPS:
# The first step for segmenting the exudates is to remove the optic disc from the image:
# 1) The optic disc mask is loaded.
# 2) The O.D. mask is dilated to make sure that it will cover all the surface of the O.D. in the RGB image.
# 3) Since the target is to remove the O.D., 1 - OD is substrated in order to get a mask where the O.D. is
# all 0s and the rest of the image is all 1s.
# 4) The O.D. is ultiplied with the green channel (since it is the one for working with the exudates)
# and now the image is already without the O.D.
# 5) Then the image is zero padded
# 6) The zero padded image histogram is calculated and can be resized in order to found the best threshold.
# 7) In the final step the image is threshold filtered and then normalized.

def opticDiscRemovalFromImage(strNumber):


    name = "IDRiD_" + str(strNumber)

    imageToRead = "path where you have the image stores" + name + ". image format (jpg, png, tif, etc)"
    image = Image.open(imageToRead)
    imageRGB = np.asarray(image, dtype =  np.uint8)
    greenImage = imageRGB[:,:,1]

    plt.imshow(imageRGB, cmap = 'gray', interpolation = 'bicubic')
    plt.xticks([]), plt.yticks([])
    plt.xlabel('RGB image')
    plt.show()


    maskToRead = "path where you have the mask with the OD stored" + name + ". mask format (jpg, png, tif, etc)"
    mask = Image.open(maskToRead)
    mask1D = np.asarray(mask, dtype =  np.uint8)

    kernelEOD = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(25,25))
    maskD = cv2.dilate(mask1D,kernelEOD,iterations = 3)

    _, zeroPad = cv2.threshold(greenImage,10,1,cv2.THRESH_BINARY)

    myImageM = greenImage*(1- maskD)
    return (myImageM, zeroPad)


def visualizeHistogram(zeroPadded):

    histrMI2 = cv2.calcHist([zeroPadded],[0], None,[256],[0,256])
    histrMI2[0:20] = 0
    plt.plot(histrMI2, color = 'g')
    plt.xlim([0,256])
    plt.grid(b=None, which='both', axis='both')
    plt.xlabel('Value [0, 256]')
    plt.ylabel('Histogram for optic disc removal')
    plt.show()

    value = int(input('Introduce the value from which you want to visualize the histogram [0-255]:  '))
    histrMI2 = cv2.calcHist([zeroPadded],[0], None,[256],[0,256])
    histrMI2[0:20] = 0
    plt.plot(histrMI2, color = 'g')
    plt.xlim([value,256])
    plt.ylim([0,np.amax(histrMI2[value:256])])
    plt.grid(b=None, which='both', axis='both')
    plt.xlabel('Value [' +str(value) + ', 256]')
    plt.ylabel('Histogram for optic disc removal')
    plt.show()

    loop = True
    while loop:

        valueChange = str(input('Do you want to change the min value from which you visualize the histogram (yes/no): '))

        if valueChange.upper() == 'YES':
            value = int(input('Introduce the new minumun value ({} is the old one)'.format(value)))
            histrMI2 = cv2.calcHist([zeroPadded],[0], None,[256],[0,256])
            histrMI2[0:20] = 0
            plt.plot(histrMI2, color = 'g')
            plt.xlim([value,256])
            plt.ylim([0,np.amax(histrMI2[value:256])])
            plt.grid(b=None, which='both', axis='both')
            plt.xlabel('Value [' +str(value) + ', 256]')
            plt.ylabel('Histogram for optic disc removal')
            plt.show()

        elif valueChange.upper() == 'NO':

            loop = False

        else:
            print('Please answer yes or no')

def filterImage(zeroPadded):

    value = int(input('Please the threshold value between 0 and 255:  '))

    _, threshImage = cv2.threshold(zeroPadded,thresh = value, maxval = 255, type =  cv2.THRESH_BINARY)
    plt.imshow(threshImage, cmap = 'gray', interpolation = 'bicubic', vmin = 0, vmax = 255)
    plt.xticks([]), plt.yticks([])
    plt.xlabel('Filtered image')
    plt.show()

    noFinish = True
    while noFinish:

        choice = str(input('Is the mask well created? (yes/no): '))

        if choice.upper() == 'YES':
            noFinish = False

        elif choice.upper() == 'NO':
            value = int(input('Introduce a new value between 0 and 255 ({} was the last value):  '.format(value)))

            if value not in range(0,255):
                print('The value has to be between 0 and 255')
                value = int(input('Introduce a new value between 0 and 255:  '))
                _, threshImage = cv2.threshold(zeroPadded, thresh = value, maxval = 255 , type = cv2.THRESH_BINARY)
                plt.imshow(threshImage, cmap = 'gray', interpolation = 'bicubic', vmin = 0, vmax = 255)
                plt.xticks([]), plt.yticks([])
                plt.xlabel('Filtered image')
                plt.show()

            else:
                _, threshImage = cv2.threshold(zeroPadded, thresh = value, maxval = 255 , type = cv2.THRESH_BINARY)
                plt.imshow(threshImage, cmap = 'gray', interpolation = 'bicubic', vmin = 0, vmax = 255)
                plt.xticks([]), plt.yticks([])
                plt.xlabel('Filtered image')
                plt.show()


        else:
            print('Please answer yes or no')

    #We normalize the image since we just want a mask with 1s and 0s
    return (threshImage/255.0)


#%%

if __name__ == '__main__':

    strNumber = str(input('Please introduce a number (from 01 to 54):  '))
    # From 01 to 54 since our training batch had a total of 54 images.

    greenWithoutDisc, zeroPad = opticDiscRemovalFromImage(strNumber)
    zeroPadded = zeroPad * greenWithoutDisc
    visualizeHistogram(zeroPadded)
    threshImage = filterImage(zeroPadded)

    plt.imshow(threshImage, cmap = 'gray', interpolation = 'bicubic')
    plt.xticks([]), plt.yticks([])
    plt.xlabel('Final mask')
    plt.show()
