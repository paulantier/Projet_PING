#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 11:13:28 2022

@author: nicolasnicolas
"""

#Importation des bibliothèques de travail
import numpy as np
import scipy
from skimage import morphology
from PIL import Image
from operator import *
import matplotlib.pyplot as plt
from drawnow import drawnow, figure

# Initialisation masque
temp_casserole = 55; #Définition de la température max d'analyse avant laquelle on considère qu'un point est un élément solide de la casserolle
bornemask = (temp_casserole + 183) / 0.007 #Equivalent en intensité de pixel de la température definie ci-dessus
vide = np.zeros((120,160),dtype = bool)
w=0

figure() #Affichage de la fenêtre 
def draw_fig():
    plt.imshow(IMG)

while(1): #Boucle qui permet de traiter les 10 images stockées successivement 
    if (w>9):
        w=0
    w+=1
    try:
        img = Image.open("%d.png"%(w)) #Variable qui stocke l'image
        I1 = np.array(img) #Conversion de cette image en tableau numpy
        [a,b,c] = np.shape(I1) #On récupère les dimensions du tableau précédent
        I2 = I1[:,:,0]*256+I1[:,:,1]+0.0 #On la convertit depuis son format 2 fois 8bit pour obtenir l'image 16 bits
        Ifull = np.full((a, b), 255) 
        Ivoid = np.zeros((a,b))
        
        imgmoins1 = Image.open("imoins1.tiff")
        I3 = np.array(imgmoins1)
        mask = np.zeros((120,160), dtype = bool)
        mask2 = np.zeros((120,160), dtype = bool) #On initialise ici deux masques qui réprésenteront respectivement la zone carrée au dessus de la casserole et la zone en dessous de la casserole qui ne nous intéresse pas dans l'encadrement.
        mask3 = np.zeros((120,160), dtype = bool)
        
        mask = I2 > bornemask #On initialise un masque des points très chauds de l'image dans le but de détecter la présence ou non d'une casserole
        casseroles = morphology.remove_small_objects(mask, min_size=40, connectivity=1) #On filtre des possibles points chauds mais trop petit pour être des casseroles.
        
        #On cherche maintenant à déterminer une zone d'intérêt qui sera la zone d'air au dessus de la casserole détectée :
        #Pour ce faire on définit une zone d'encadrement de la casserole dans les deux coordonnées de l'image.
        #On initialise les valeurs des maximums avant de faire des calculs pixel par pixel
        min_i=120
        min_j=160
        max_i=0
        max_j=0
        imax_j=120
        imin_j=120
        
        for j in range(1, 160): #Pour tout pixel de chaque image
            for i in range(1, 120):
                if (casseroles[i][j] == 1):
                    max_i = max(i,max_i)
                    max_j = max(j,max_j)
                    min_i = min(i,min_i)
                    min_j = min(j,min_j)
                    if (max_j == j):
                        imax_j=i #On note la coordonnée i de la matrice pour laquelle j est maximale
                    if (min_j == j):
                        imin_j=i #de même avec j minimale
        
        ffbord = max(1,min_i-70) #Précaution pour éviter des problèmes d'indices aux bords
        mask2[ffbord:max_i,min_j:max_j] = True
        mask3[min(imax_j,imin_j):120,min_j:max_j] = True
        masktest = np.logical_and(mask2,np.logical_not(mask3)) 
        mask4 = np.maximum(vide,masktest) #le masque 4 permet de travailler avec une matrice booléenne.
        maskfinal = np.logical_and(mask4,np.logical_not(casseroles)) 
      
        Itest = np.maximum(Ivoid,np.subtract(I2, I3))
        I4 = np.minimum(Itest,Ifull) #On calcule la soustraction de notre matrice à l'instant t moins celle à l'instant t-1.
        I5 = I4[:,:] > 38 #On effectue un seuillage global pour convertir en binaire cette image
        I6 = morphology.remove_small_objects(I5, min_size=10, connectivity=1) #On utilise une opération morphologique pour supprimer les tas de pixels bruités. Cet outil de morphologie permet de supprimer les zones de pixels ayant une aire inférieure à une constante
        I7 = np.logical_and(I5,np.logical_not(I6)) #I7 contient la position des pixels bruités
        I4 = I4*np.logical_not(I7) #Que l'on supprime ensuite sur notre image de soustraction
        
        I8 = I4[:,:] > 26 #On réeffectue la même opération avec un seuil binaire différent
        I9 = morphology.remove_small_objects(I8, min_size=15, connectivity=1)
        I10 = np.logical_and(I8,np.logical_not(I9))
        I4 = I4*np.logical_not(I10)
        I11 = I4[:,:] > 13 #On refait un dernière seuillage binaire pour enlever les pixels de valeur négligeable
        I12 = np.logical_and(I11,np.logical_not(I8))
        I4 = I4*np.logical_not(I12)
        I4 = I4*I11 
        I4 = I4*maskfinal
        
        IMG = Image.fromarray(I4.astype(np.uint8))
        IMGmoins1 = Image.fromarray(I2.astype(np.uint16))
        nomRes = "imoins1.tiff"
        IMGmoins1.save(nomRes)
        drawnow(draw_fig)
        
    except:
        pass
