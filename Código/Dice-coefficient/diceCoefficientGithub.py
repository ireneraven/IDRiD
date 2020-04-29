#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 00:57:12 2020

@author: andreagrande
"""


from PIL import Image
import tensorflow as tf
from skimage import io
import numpy as np
from keras import backend as K

# %% DISCO OPTICO
im1=Image.open('/Users/andreagrande/Documents/INGENIERIA BIOMEDICA/4 CARRERA/PROCESADO/OD-Presentación/IDRiD_49_OD_US.jpg')
im2=Image.open('/Users/andreagrande/Documents/INGENIERIA BIOMEDICA/4 CARRERA/PROCESADO/A. Segmentation/2. All Segmentation Groundtruths/a. Training Set/5. Optic Disc/IDRiD_49_OD.tif')

# %% EXUDADOS
im1=Image.open('/Users/andreagrande/Documents/INGENIERIA BIOMEDICA/4 CARRERA/PROCESADO/EX-Presentación/IDRiD_03_EX_US.jpg')
im2=Image.open('/Users/andreagrande/Documents/INGENIERIA BIOMEDICA/4 CARRERA/PROCESADO/A. Segmentation/2. All Segmentation Groundtruths/a. Training Set/3. Hard Exudates/IDRiD_03_EX.tif')


# %% HEMORRAGIAS
im1=Image.open('/Users/andreagrande/Documents/INGENIERIA BIOMEDICA/4 CARRERA/PROCESADO/1.png')
im2=Image.open('/Users/andreagrande/Documents/INGENIERIA BIOMEDICA/4 CARRERA/PROCESADO/2.png')

# %%
def dice(im1, im2, empty_score=1.0):
   
    im1 = np.asarray(im1).astype(np.bool)
    im2 = np.asarray(im2).astype(np.bool)

    if im1.shape != im2.shape:
        raise ValueError("Shape mismatch: im1 and im2 must have the same shape.")

    im_sum = im1.sum() + im2.sum()
    if im_sum == 0:
        return empty_score

    # Compute Dice coefficient
    intersection = np.logical_and(im1, im2)

    return 2. * intersection.sum() / im_sum


# %%
    
print(dice(im1, im2, 1.0))






