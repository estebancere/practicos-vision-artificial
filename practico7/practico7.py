import cv2 as cv
import numpy as np
import math

img = cv.imread('ramones.jpg')

def rotateandtranslate(imagen, angulo, x, y,escala):

    angulo=math.radians(angulo)

    matriz_rot_tras=np.float32([[escala*math.cos(angulo), escala*math.sin(angulo),x],
                                [-escala*math.sin(angulo), escala*math.cos(angulo), y]])

    rotada_trasladada=cv.warpAffine(imagen,matriz_rot_tras,(1366,768))
    return rotada_trasladada


while True:
    imagen_rotada_trasladada=rotateandtranslate(img,35,100,300,1.5)
    cv.imshow('practico6', imagen_rotada_trasladada)
    k = cv.waitKey(20) & 0xFF
    if k == ord('q'):
        cv.destroyAllWindows()
        break