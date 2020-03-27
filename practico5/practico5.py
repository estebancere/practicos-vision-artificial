import cv2 as cv
import numpy as np

img = cv.imread('ramones.jpg')


def dibujar(event, x, y, flags, params):
    global ix, iy, imgcortada
    if event == cv.EVENT_LBUTTONDOWN:
        ix, iy = x, y
    elif event == cv.EVENT_LBUTTONUP:
        cv.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 3)
        imgcortada = img[iy:y, ix:x]


cv.namedWindow("practico5")
cv.setMouseCallback("practico5", dibujar)

while True:
    cv.imshow('practico5', img)
    k = cv.waitKey(20) & 0xFF
    if k == ord('r'):
        img = cv.imread('ramones.jpg')
        cv.imshow('practico5', img)
    elif k == ord('g'):
        cv.imwrite('imagen_cortada.jpg', imgcortada)
        cv.destroyAllWindows()
        break
    elif k == ord('q'):
        cv.destroyAllWindows()
        break
