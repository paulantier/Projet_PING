#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 11:13:28 2022

@author: nicolasnicolas
"""

import numpy as np
import scipy
from skimage import morphology
from PIL import Image
from operator import *
import matplotlib.pyplot as plt
from drawnow import drawnow, figure

import RPi.GPIO as GPIO
# pour les tests
#import time


def controlevitesse(n):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    sortie1 = 4
    sortie2 = 5
    if (n == 0):
        GPIO.setup(sortie1,GPIO.OUT)
        GPIO.output(sortie1,0)
        GPIO.setup(sortie2,GPIO.OUT)
        GPIO.output(sortie2,0)
    if(n==1):
        GPIO.setup(sortie1,GPIO.OUT)
        GPIO.output(sortie1,1)
        GPIO.setup(sortie2,GPIO.OUT)
        GPIO.output(sortie2,0)
    if(n==2):
        GPIO.setup(sortie1,GPIO.OUT)
        GPIO.output(sortie1,1)
        GPIO.setup(sortie2,GPIO.OUT)
        GPIO.output(sortie2,1)

# Initialisation masque
temp_casserole = 55;
bornemask = (temp_casserole + 183) / 0.007
vide = np.zeros((120,160),dtype = bool)
w=0
moytotal=0
nosmoke = Image.open("pasfumee.png")
pasfumee = np.array(nosmoke)

figure()
def draw_fig():
    plt.imshow(IMG)

while(1):
    if (w>9):
        w=0
    w+=1
    try:
        img = Image.open("%d.png"%(w))
        I1 = np.array(img)
        [a,b,c] = np.shape(I1)
        I2 = I1[:,:,0]*256+I1[:,:,1]+0.0
        Ifull = np.full((a, b), 255) 
        Ivoid = np.zeros((a,b))
        
        imgmoins1 = Image.open("imoins1.tiff")
        I3 = np.array(imgmoins1)
        mask = np.zeros((120,160), dtype = bool)
        mask2 = np.zeros((120,160), dtype = bool)
        mask3 = np.zeros((120,160), dtype = bool)
        
        mask = I2 > bornemask
        casseroles = morphology.remove_small_objects(mask, min_size=40, connectivity=1)
        min_i=120
        min_j=160
        max_i=0
        max_j=0
        imax_j=120
        imin_j=120
        
        for j in range(1, 160):
            for i in range(1, 120):
                if (casseroles[i][j] == 1):
                    max_i = max(i,max_i)
                    max_j = max(j,max_j)
                    min_i = min(i,min_i)
                    min_j = min(j,min_j)
                    if (max_j == j):
                        imax_j=i
                    if (min_j == j):
                        imin_j=i
        
        ffbord = max(1,min_i-70)
        mask2[ffbord:max_i,min_j:max_j] = True
        mask3[min(imax_j,imin_j):120,min_j:max_j] = True
        masktest = np.logical_and(mask2,np.logical_not(mask3)) 
        mask4 = np.maximum(vide,masktest)
        maskfinal = np.logical_and(mask4,np.logical_not(casseroles)) 
      
        Itest = np.maximum(Ivoid,np.subtract(I2, I3))
        I4 = np.minimum(Itest,Ifull)
        I5 = I4[:,:] > 38
        I6 = morphology.remove_small_objects(I5, min_size=10, connectivity=1)
        I7 = np.logical_and(I5,np.logical_not(I6))
        I4 = I4*np.logical_not(I7)
        
        I8 = I4[:,:] > 26
        I9 = morphology.remove_small_objects(I8, min_size=15, connectivity=1)
        I10 = np.logical_and(I8,np.logical_not(I9))
        I4 = I4*np.logical_not(I10)
        I11 = I4[:,:] > 13
        I12 = np.logical_and(I11,np.logical_not(I8))
        I4 = I4*np.logical_not(I12)
        I4 = I4*I11 
        I4 = I4*maskfinal
        
        moy=I4.mean()
        if moy<0.5:
            I4=pasfumee
            
        moytotal=(moytotal*9+moy)/10
        if moytotal >5:
            controlevitesse(2)
        elif moytotal>1:
            controlevitesse(1)
        else:
            controlevitesse(0)
        
        IMG = Image.fromarray(I4.astype(np.uint8))
        IMGmoins1 = Image.fromarray(I2.astype(np.uint16))
        nomRes = "imoins1.tiff"
        IMGmoins1.save(nomRes)
        drawnow(draw_fig)
        
    except:
        pass
