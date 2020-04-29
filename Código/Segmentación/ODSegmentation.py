# -*- coding: utf-8 -*-

#%%

from PIL import Image
import cv2
import numpy as np
from matplotlib import pyplot as plt


#%%

def chooseChannel(image):

    #Lets choose which image we want to work with
    imagesList = [image[:,:,0], image[:,:,2]]
    imageTitles = ('Red channel', 'Blue channel')

    for i,img in enumerate(imagesList):
        plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
        plt.xticks([]), plt.yticks([])
        plt.xlabel(imageTitles[i])
        plt.show()

    choose = True
    while choose:

        election = str(input('Choose in which channel is easier to diferentiate the optic disc (red or blue): ')).upper()


        if election == 'RED':
            myImage = cv2.medianBlur(image[:,:,0], 205)
            choose = False

        elif election == 'BLUE':
            myImage = cv2.medianBlur(image[:,:,2], 205)
            choose = False

        else:
            print('Please choose blue or red')
            election = str(input('Choose in which channel is easier to diferentiate the optic disc (red or blue)')).upper()

    return (myImage)

def histrogramThresholding(zeroPadded, myMask):
    #Now we will calculate the histrogram for filtering with the threshold:
    histrR = cv2.calcHist([zeroPadded],[0], None,[256],[0,256])
    histrR[0] = 0

    #Now lets see if the automatical threshold is working assuming that the optic disc is the 2.5% of the eye area
    sumV = 0
    minThresh = 0
    for i in range(len(histrR)):
        sumV += histrR[255-i]
        if (sumV/sum(histrR)*100) > 2.5:
            minThresh = 256-i
            break

    dst	= cv2.inRange(zeroPadded, minThresh, 256)
    opticDisc = (dst /255)* myMask

    plt.imshow(opticDisc, cmap = 'gray', interpolation = 'bicubic')
    plt.xticks([]), plt.yticks([])
    plt.xlabel('Optic disc first ')
    plt.show()

    plt.imshow(image, cmap = 'gray', interpolation = 'bicubic')
    plt.xticks([]), plt.yticks([])
    plt.xlabel('Original image')
    plt.show()

    choose = True
    while choose:

        election = str(input('Is the segmented optic disc almost the same as the original one (yes/no): ')).upper()

        if election == 'YES':
            choose = False

        elif election == 'NO':
            plt.plot(histrR, color = 'g')
            plt.xlim([0,265])
            plt.grid(b=None, which='both', axis='both')
            plt.xlabel('Value [0, 256]')
            plt.ylabel('Histogram for optic disc removal')
            plt.show()

            minThresh = int(input('The automatic threshold was {}, please choose another min value for thresholding: '.format(minThresh)))
            dst	= cv2.inRange(zeroPadded, minThresh, 256)
            opticDisc = (dst /255)* myMask

            plt.imshow(opticDisc, cmap = 'gray', interpolation = 'bicubic')
            plt.xticks([]), plt.yticks([])
            plt.xlabel('Optic disc first ')
            plt.show()

            plt.imshow(image, cmap = 'gray', interpolation = 'bicubic')
            plt.xticks([]), plt.yticks([])
            plt.xlabel('Original image')
            plt.show()

        else:
            print('Please write yes or no')

    return (opticDisc)


def removingNonOD(opticDisc):

    suitableImage = ((opticDisc / np.amax(opticDisc))*255).astype(np.uint8)

    #Retval gives me the number of conected items greater than a (3x3) shape since I use connectivity = 8
    retval, labels=cv2.connectedComponents(suitableImage,connectivity = 8)



    contador = 0
    while retval > 2:
    #Retval has to be two because one is for the background and another for the optic disc:
        print('Deleting components that are not the optic disc')
        kernelEOD = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15))
        opticDiscE = cv2.erode(opticDisc,kernelEOD,iterations = 8)
        suitableImage = ((opticDiscE / np.amax(opticDiscE))*255).astype(np.uint8)
        retval, labels= cv2.connectedComponents(suitableImage,connectivity = 8)
        contador += 1

    if contador > 0:
        opticDiscD = cv2.dilate(opticDiscE,kernelEOD,iterations = 8*contador)

    else:
        opticDiscD = opticDisc

    plt.imshow(opticDiscD, cmap = 'gray', interpolation = 'bicubic')
    plt.xticks([]), plt.yticks([])
    plt.xlabel('Final optic disc')
    plt.show()

    choose = True
    while choose:

        election = str(input('Is the final optic smaller original one (yes/no): ')).upper()

        if election == 'NO':
            choose = False
            print('Segmentation finalized')

        elif election == 'YES':
            kernelEOD = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15))
            opticDiscE = cv2.erode(opticDiscD,kernelEOD,iterations = 1)
            opticDiscD = cv2.dilate(opticDiscE,kernelEOD,iterations = 2)

            plt.imshow(opticDiscD, cmap = 'gray', interpolation = 'bicubic')
            plt.xticks([]), plt.yticks([])
            plt.xlabel('Enhanced final optic disc')
            plt.show()

        else:
            print('Please write yes or no')

    return(opticDiscD)



def getOpticDisc(image):


    print('Starting segmentation')

    myImage = chooseChannel(image)
    ret, myMask = cv2.threshold(image[:,:,0],7,1,cv2.THRESH_BINARY)
    zeroPadded = myImage * myMask
    opticDisc = histrogramThresholding(zeroPadded, myMask)
    opticDiscD = removingNonOD(opticDisc)


    return(opticDiscD)


#%%
if __name__ == '__main__':

    imageToRead = "path"
    image = Image.open(imageToRead)
    imageRGB = np.asarray(image, dtype =  np.uint8)
    opticDiscD = getOpticDisc(imageRGB)

    plt.imshow(opticDiscD, cmap = 'gray', interpolation = 'bicubic')
    plt.xticks([]), plt.yticks([])
    plt.xlabel('Dilated optic disc')
    plt.show()
