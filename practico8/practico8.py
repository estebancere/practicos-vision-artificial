import cv2 as cv
import numpy as np

imagen = cv.imread('ramones.jpg')
imagen_incrustar = cv.imread("andres.jpg")

i = 0
x0 = 0
y0 = 0
x1 = 0
y1 = 0
x2 = 0
y2 = 0


def dibujar(event, x, y, flags, params):
    global x0, y0, x1, y1, x2, y2, i
    if event == cv.EVENT_LBUTTONDOWN:
        if i == 0:
            x0, y0 = x, y
            cv.circle(imagen, (x0, y0), 3, (255, 0, 0), -1)
            i = i + 1
        elif i == 1:
            x1, y1 = x, y
            cv.circle(imagen, (x1, y1), 3, (255, 0, 0), -1)
            i = i + 1
        elif i == 2:
            x2, y2 = x, y
            cv.circle(imagen, (x2, y2), 3, (255, 0, 0), -1)
            i = 4


cv.namedWindow("practico8")
cv.setMouseCallback("practico8", dibujar)

while True:
    cv.imshow("practico8", imagen)
    if i==4:
        dst_triangle = np.float32([[x0, y0],[x1, y1],[x2, y2]])
        src_triangle = np.float32([[0, 0],[imagen_incrustar.shape[1], 0],[0, imagen_incrustar.shape[0]]])
        M = cv.getAffineTransform(src_triangle, dst_triangle)
        incrustada = cv.warpAffine(imagen_incrustar, M, (imagen.shape[1], imagen.shape[0]))
        incrustada_grey=cv.cvtColor(incrustada,cv.COLOR_BGR2GRAY)
        ret, mask = cv.threshold(incrustada_grey, 10, 255, cv.THRESH_BINARY)
        mask_invertida=cv.bitwise_not(mask)
        imagen_enmascarada=cv.bitwise_and(imagen,imagen,mask=mask_invertida)
        incrustada_enmascarada=cv.bitwise_and(incrustada,incrustada,mask=mask)
        imagen_final=cv.add(imagen_enmascarada,incrustada_enmascarada)
        cv.imshow('incrustada', imagen_final)
        i=0
    if cv.waitKey(20) & 0xFF == 27:
        break
cv.destroyAllWindows()
