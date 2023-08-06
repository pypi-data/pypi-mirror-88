import os
import pandas as pd
import xlwt
import lxml
from lxml import etree
from datetime import datetime
from xlwt import *
import xlsxwriter
import math
from os import listdir
import numpy as np
import sys
import cv2
import numpy as np
#from matplotlib import pyplot as plt


def generaExcel(carpeta, es, pixeles, unidad ):
    wb = xlsxwriter.Workbook(carpeta+'/'+'glandulas.xlsx')
    ws = wb.add_worksheet('Glandulas')

    style0 = wb.add_format({'bold': True, 'font_color': 'white', 'fg_color': '0x10'})
    # style0.set_font_color('red')
    # -------------------------------------
    path = carpeta
    lstFiles = []
    lstImgs = []
    lstDir = os.walk(path)  # os.walk()
    for root, dirs, files in lstDir:
        for fichero in files:
            (nombreFichero, extension) = os.path.splitext(fichero)
            if (extension == ".xml"):
                lstFiles.append(nombreFichero + extension)
                lstImgs.append(nombreFichero+".jpg")

    i = 1
    col = 0
    lstFiles.sort()
    ws.write(0, 0, 'Image name', style0)
    ws.set_column(0, 0, 25)
    ws.write(0, 1, 'Number of glandulas in total', style0)
    ws.set_column(0, 1, 20)
    ws.write(0, 2, 'Average area'+" {}²".format(unidad), style0)
    ws.set_column(0, 2, 20)
    ws.write(0, 3, 'area cubierta'+" {}²".format(unidad), style0)
    ws.set_column(0, 3, 20)
    ws.write(0, 4, 'area folial'+" {}²".format(unidad), style0)
    ws.set_column(0, 4, 20)
    ws.write(0, 5, 'cubierta/folial'+" {}²".format(unidad), style0)
    ws.set_column(0, 5, 20)
    ws.write(0, 6, 'cel/folial'+" {}²".format(unidad), style0)
    ws.set_column(0, 6, 20)
    ws.write(0, 7, 'mediana'+" {}²".format(unidad), style0)
    ws.set_column(0, 7, 20)
    ws.write(0, 8, 'max'+" {}²".format(unidad), style0)
    ws.set_column(0, 8, 20)
    ws.write(0, 9, 'min'+" {}²".format(unidad), style0)
    ws.set_column(0, 9, 20)
    #print(es)
    #print(pixeles)
    escala = es/ pixeles
    #print(escala)
    for fichero in lstFiles:
        (nomFich, ext) = os.path.splitext(fichero)
        image = cv2.imread(path+"/"+nomFich+".jpg")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('gray', gray)
        ret, thresh1 = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
        #cv2.imshow('bina',thresh1)
        contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_area =0
        height, width, channels = image.shape
        areaTo = height*width
        # calculate area and filter into new array
        for con in contours:
            area = cv2.contourArea(con)
            contours_area = contours_area+area

        #print(nomFich+" "+str(areaTo-contours_area))

        #plt.imshow(th1,"gray")

        numGlan = 0
        j = 0
        k = 0
        # alturaTotal = 0
        # anchuraTotal = 0
        listaArea = []
        doc = etree.parse(carpeta+'/' + fichero)
        filename = doc.getroot()  # buscamos la raiz de nuestro xml
        nomImagen = filename.find("filename")
        # print(filename.text)  # primer elto del que obtenemos el título de nuestro video
        # ws.write(i, 0, nomImagen.text.split('\\')[len(nomImagen.text.split('/'))-1])
        ws.write(i, 0, nomFich+".jpg")
        objetos = filename.findall("object")
        j =0
        if len(objetos)==0:
            listaArea.append(0)
        else:
            while j < len(objetos):
                if objetos[j].find("name").text == "glandula":
                    areaGlan =0
                    # stoma = objetos[j].find("name")
                    #numero de glandulas por imagen
                    numGlan = numGlan + 1
                    ymax = float(objetos[j].find("bndbox").find("ymax").text)
                    ymin = float(objetos[j].find("bndbox").find("ymin").text)
                    xmax = float(objetos[j].find("bndbox").find("xmax").text)
                    xmin = float(objetos[j].find("bndbox").find("xmin").text)

                    anchura = (xmax - xmin)
                    altura = (ymax - ymin)
                    areaGlan = (anchura*altura)
                    #ws.write(0, 9 + 2 * k, 'Height' + str(k) + '('+unidad+')', style0)

                    listaArea.append(areaGlan)
                    #ws.write(0, 9 + 2 * k + 1, 'Width' + str(k) + '('+unidad+')', style0)



                    k = k + 1



                j = j + 1

        ws.write(i, 1, numGlan)
        #else:
            #col = col +1
        #print(listaArea)
        areamedia = np.mean(listaArea)
        areaCubierta = np.sum(listaArea)
        areaFolial = areaTo-contours_area
        prueba = float('%.4f' % (areamedia*escala*escala))
        ws.write(i, 2, prueba)
        ws.write(i, 3, float('%.4f' % (areaCubierta*escala*escala)))
        ws.write(i, 4, float('%.4f' % (areaFolial*escala*escala)))
        ws.write(i, 5, float('%.10f' % ((areaCubierta/areaFolial))))
        ws.write(i, 6, float('%.10f' % ((numGlan/(areaFolial*escala*escala)))))
        ws.write(i, 7, float('%.10f' % (np.median(listaArea)*escala*escala)))
        ws.write(i, 8, float('%.10f' % (np.max(listaArea)*escala*escala)))
        ws.write(i, 9, float('%.10f' % (np.min(listaArea)*escala*escala)))
        i = i + 1
    wb.close()
    # wb.save('UsueEstomas.xlsx')