# -*- coding: utf-8 -*-

# Since we will be working with arrays, instead of loading the photos we will directly load an array with
# all the photo transformations.

#%%
#Importar los módulos
import numpy as np
import os
from PIL import Image
from tqdm import tqdm

#%%
# CHANGE r'/' to r'//' if using Windows

def getImageDepth(path, filesInPath):
    
    imageFormat = np.ndim(Image.open(path + r'/' + filesInPath[-1]))
    
    if imageFormat == 2:       
        depthValue = 1
    else:
        depthValue = np.asarray(Image.open(path + r'/' + filesInPath[-1])).shape[-1]

    return(depthValue)


def getDataIntoArray(path):

    filesInPath = os.listdir(path)    
    depthValue = getImageDepth(path, filesInPath)   
    
    arrayOfImages = np.zeros((len(filesInPath)*16, 512, 512, depthValue), dtype=np.float32)
    
    degrees = [0, 45, 90, 135, 180, 225, 270, 315]

    for i, filename in tqdm(enumerate(filesInPath)):
        imageName = filename.split('.') #We get [image name, image format]

        imageToRead = path + r'/' + str(imageName[0]) + '.' + imageName[1]
        img = Image.open(imageToRead)
        
        for j, degree in enumerate(degrees):                    
            #----------------------------------------------------------#  
            
            rotatedImage = img.rotate(degree, expand = True)
            imgResiz = rotatedImage.resize((512, 512), resample = 3)  
            #----------------------------------------------------------#   
            
            imgRotated = (np.asarray(imgResiz))/np.amax(img)   
            mirrorImage = np.fliplr(imgRotated) #changes columns
            #----------------------------------------------------------#  
            
            R1 = np.resize(imgRotated,(512, 512, depthValue))
            R2 = np.resize(mirrorImage,(512, 512, depthValue))
            #----------------------------------------------------------#
            
            arrayOfImages[(16*i) + (j*2)] = R1
            arrayOfImages[(16*i) + ((j*2)+1)] = R2


    return(arrayOfImages)


#%%
# Change the name of the paths and write the corresponding ones.

def loadAndSaveArrays():
    arraysNames = ['X_train', 'X_test', 'y_train_OD', 'y_test_OD', 'y_train_HE', 'y_test_HE', 'y_train_EX', 'y_test_EX', 'y_train_MA', 'y_test_MA']
    correspondingPaths = ['path_X_train',
                          'path_X_test',
                          'path_y_train_OD',
                          'path_y_test_OD',
                          'path_y_train_HE',
                          'path_y_test_HE',
                          'path_y_train_EX',
                          'path_y_test_EX',
                          'path_y_train_MA',
                          'path_y_test_MA',
                          
                          ]

    for i in range(len(arraysNames)):
        
        arrayToSave = getDataIntoArray(correspondingPaths[i]) 
        
        np.save('derired_path' + r'/' + arraysNames[i] + '.npy', arrayToSave)
        
#%%
# Here the function will load all the arrays and save them in an specific file. 

if __name__ == '__main__':
    print('This process will take some time')
    loadAndSaveArrays()      
