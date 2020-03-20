#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
import cv2
img = cv2 . imread ('cuatrohojasverdes.PNG',0)

for i , row in enumerate ( img ) :
    for j , col in enumerate ( row ) :
        if img[i,j]>150:
            img[i,j]=255
        else:
            img[i,j]=0



cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
# Agregar código aquí
# Para resolverlo podemos usar dos for anidados
#cv2 . imwrite ( ' resultado.png' , img )