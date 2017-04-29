#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Watermarkero, Mario, Ariel
"""

from PIL import Image
import random
import matplotlib.pyplot as plt
import numpy as np

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def marcarPixel(color, bitporinsertar):
    if (color%2)==1:
        if bitporinsertar==0:
            color=color-1
    elif (color%2)==0:
        if bitporinsertar==1:
            color=color+1
    return color

def plotLsbRgb(img):
    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.set_title('Imagen RGB')
    ax1.imshow(img)
    ax2.set_title('LSB RGB')
    img=255*(img%2)
    ax2.imshow(img)
    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10,
                        right=0.95, hspace=0.3,wspace=0.35)

#imagen original
path="img3.jpg"
imgOriginal = np.array(Image.open(path))
nFilas, nCols, nCanales = imgOriginal.shape
#marca
key=41196
random.seed(key)
porcentajeDeimagenPorMarcar=50
sizeMarca = nCols*int(porcentajeDeimagenPorMarcar*(nFilas/100))
#marca = [random.randint(0,1) for i in range(sizeMarca)]
plotLsbRgb(imgOriginal)

#proceso de marcado
imgMarcada = imgOriginal.copy();
cont = 1 #contador del numero de bits inscrustados
#Proceso de incrustacion
for fila in range(0,nFilas):
    for columna in range(0,nCols):
        pixel=imgOriginal[fila,columna]
        newPixel = [marcarPixel(
            pixel[0],random.randint(0,1)),
            marcarPixel(pixel[1],random.randint(0,1)),
            marcarPixel(pixel[2],random.randint(0,1))]
        imgMarcada[fila,columna] = newPixel
        if cont >= sizeMarca:
            break
        cont = cont +1
    if cont >= sizeMarca:
        break        

plotLsbRgb(imgMarcada)
image = Image.fromarray(imgMarcada, 'RGB')
image.save('ImagenMarcada.bmp')
print('Porciento de la imagen marcada: ' + str(porcentajeDeimagenPorMarcar)+'%')
print('bits incrustados: ' + str(sizeMarca*3))
print('Bytes incrustados: ' + str(sizeMarca*3/8))
print('KiloBytes incrustados: ' + str(sizeMarca*3/8/1024))
print('MegaBytes incrustados: ' + str(sizeMarca*3/8/1024/1024))
