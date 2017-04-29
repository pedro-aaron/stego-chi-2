#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Watermarkero, Mario, Ariel
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from PIL import Image

#los valores esperados en el promedio de cada PoV
def valoresEsperados (observed):
    expected=[]
    for i in range(0,256,2):
        observedN=observed[i]
        observedNplus1=observed[i+1]
        expectedValuePoV=(observedN+observedNplus1)/2
        expected.append(expectedValuePoV)
        expected.append(expectedValuePoV)
    return np.float64(np.array(expected))

#los valores observados son los PoV...un histograma
def valoresObservados(muestra):
    observed, bin_edges = np.histogram(muestra, bins=list(range(257))) 
    return np.float64(np.array(observed))

#Cálculo de chiCuadrada en las tablas esperadas y observadas
def chiSquare(observed, expected, degreesOfFreedom):
    chi_squared_stat = (((observed-expected)**2)/expected).sum()
    p_value = 1 - stats.chi2.cdf(x=chi_squared_stat, df=degreesOfFreedom)
    return p_value

#test chi-2 sobre el LSB de la imagen
def chiSquareOnImage(imgGray, show=False):
    nFilas, nCols = imgGray.shape
    chiSquareLsb=[]
    promedioLsb=[]
    if show: #debug
        cont=1
    for step in range(1,101):
        #obtener la muestra de pixeles y su LSB
        filaMax=int(step*(nFilas/100))
        muestra = imgMarcadaR[0:filaMax,:]
        muestraLsb=muestra%2
        #promedio de 1's y 0's 
        promedioMuestra=(muestraLsb.sum()/(muestraLsb.size))
        promedioLsb.append(promedioMuestra)
        #se calculan los valores observados y esperados de PoV
        observed=valoresObservados(muestra)
        expected=valoresEsperados(observed)        
        #se eliminan los elementos con valor esperado 0, para evitar que el chi-2
        #no tenga divisiones por cero
        expectedMasked=np.ma.masked_equal(expected,0)
        expectedFinal=expectedMasked.compressed()
        mascara=np.ma.getmask(expectedMasked)
        observedMasked = np.ma.array(observed, mask=mascara)
        observedFinal=observedMasked.compressed()
        #se calcula el test chi-2
        p_value = chiSquare(observedFinal,expectedFinal,(observedFinal.size/2)-1)
        chiSquareLsb.append(p_value)
        if show: #debug
            print('muestra: ' + str(cont) + ' - fila:' + str(filaMax) + ':' + str(nFilas))
            cont=cont+1
    return chiSquareLsb,promedioLsb
    

def plotChiSquare1(chiSquareLsb, promedioLsb,fileName="chi-2.png"):
    plt.figure()
    plt.xlabel('tamaño de la muestra')
    plt.ylabel('p-value del test Chi-2')
    plt.title('Test Chi-2 en estegoanálisis')
    plt.plot(promedioLsb,'go', markersize=1)
    plt.plot(chiSquareLsb,'ro', markersize=1)
    plt.axis([-5, 105, -0.1, 1.1])
    plt.grid(True)
    plt.show()
    plt.savefig(fileName)

def plotChiSquare3(chiR, promR, chiG, promG, chiB, promB):
    figw, figh = 8.0, 6.0
    fig, (ax1, ax2, ax3) = plt.subplots(ncols=1, nrows=3, sharex=True, sharey=True,
                             figsize=(figw, figh))
    ax1.set_ylabel('p-value')
    ax1.set_title('Test Chi-2 en en canal R')   
    ax1.plot(promR,'go', markersize=3)
    ax1.plot(chiR,'ro', markersize=3)
    ax1.axis([-5, 105, -0.1, 1.1])
    ax1.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
    ax2.set_ylabel('p-value')
    ax2.set_title('Test Chi-2 en en canal G')
    ax2.plot(promG,'go', markersize=3)
    ax2.plot(chiG,'ro', markersize=3)
    ax2.axis([-5, 105, -0.1, 1.1])
    ax2.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
    ax3.set_xlabel('tamaño de la muestra')
    ax3.set_ylabel('p-value')
    ax3.set_title('Test Chi-2 en en canal B')
    ax3.plot(promB,'go', markersize=3)
    ax3.plot(chiB,'ro', markersize=3)
    ax3.axis([-5, 105, -0.1, 1.1])
    ax3.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)


    
path='img3.jpg'
imgMarcada = np.array(Image.open(path))
imgMarcadaR=imgMarcada[:,:,0]
imgMarcadaG=imgMarcada[:,:,0]
imgMarcadaB=imgMarcada[:,:,0]

chiSquareLsbR, promedioLsbR = chiSquareOnImage(imgMarcadaR,True)
chiSquareLsbG, promedioLsbG = chiSquareOnImage(imgMarcadaG,True)
chiSquareLsbB, promedioLsbB = chiSquareOnImage(imgMarcadaB,True)
#plotChiSquare1(chiSquareLsbR, promedioLsbR)
#plotChiSquare1(chiSquareLsbG, promedioLsbG)
#plotChiSquare1(chiSquareLsbB, promedioLsbB)

plotChiSquare3(chiSquareLsbR, promedioLsbR,chiSquareLsbG, promedioLsbG,chiSquareLsbB, 
               promedioLsbB)