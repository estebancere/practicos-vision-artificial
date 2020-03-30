import cv2 as cv
import numpy as np

imagen = cv.imread('puchos.jpg')

i = 0
x0 = 0
y0 = 0
x1 = 0
y1 = 0
x2 = 0
y2 = 0
x3 = 0
y3 = 0

rows, cols, channel= imagen.shape

def dibujar(event, x, y, flags, params):
    global x0, y0, x1, y1, x2, y2,x3,y3, i
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
            i = i + 1
        elif i == 3:
            x3, y3 = x, y
            cv.circle(imagen, (x3, y3), 3, (255, 0, 0), -1)
            i = 4


cv.namedWindow("practico9")
cv.setMouseCallback("practico9", dibujar)

while True:
    cv.imshow("practico9", imagen)
    if i == 4:
        fuente = np.float32([[x0, y0], [x1, y1], [x2, y2],[x3,y3]])
        destino= np.float32([[0, 0], [300, 0],[300,300], [0, 300]])
        matriz = cv.getPerspectiveTransform(fuente,destino)
        mostrar=cv.warpPerspective(imagen,matriz,(300,300))
        cv.imshow('mostrar',mostrar)
        i=0
    if cv.waitKey(20) & 0xFF == 27:
        break
cv.destroyAllWindows()
