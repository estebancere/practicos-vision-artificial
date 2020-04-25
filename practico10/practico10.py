import cv2 as cv
import numpy as np
from imutils import perspective
from imutils import contours

#función para calcular punto medio entre dos puntos
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

#importo la imagen original
imagen_original = cv.imread('medir.jpeg')

#paso la imagen a gris
imagen_gris = cv.cvtColor(imagen_original, cv.COLOR_BGR2GRAY)

#filtro gausiano
imagen_gris = cv.GaussianBlur(imagen_original, (7, 7), 0)

#la función canny detecta bordes
imagen_bordeada = cv.Canny(imagen_gris, 20, 180)

#devuelve un arreglo contornos cerrados
contornos, hierarchy = cv.findContours(imagen_bordeada, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

#dibujo el contorno 6 en la imagen original que es el del papel glase
cv.drawContours(imagen_original, contornos, 6, (0, 255, 0), 2)

#recorro todo el arreglo de los contornos cerrados que encontro la función
for x, contorno in enumerate(contornos):
    #si el contorno es el 6, es decir, es el papel glasé
    if x ==6:
        #obtengo las coordenadas de  los puntos máximos y mínimos en X y en Y
        punto_izquierda_abajo = tuple(contorno[contorno[:, :, 0].argmin()][0])
        punto_derecha_arriba = tuple(contorno[contorno[:, :, 0].argmax()][0])
        punto_izquierda_arriba = tuple(contorno[contorno[:, :, 1].argmin()][0])
        punto_derecha_abajo = tuple(contorno[contorno[:, :, 1].argmax()][0])

        #ahora hacemos una matriz con los vértices del papel
        vertices_in = np.float32([
            # vértice superior izquierdo (coordenadas del mínimo punto en y)
            [punto_izquierda_arriba[0], punto_izquierda_arriba[1]],
            # vértice superior derecho (coordenas del máximo punto en x)
            [punto_derecha_arriba[0], punto_derecha_arriba[1]],
            # vértice inferior derecho (coordenadas del máximo punto en y)
            [punto_derecha_abajo[0], punto_derecha_abajo[1]],
            # vértice inferior izquiero (coordenadas del mínimo punbto en y)
            [punto_izquierda_abajo[0], punto_izquierda_abajo[1]]
        ])
        #ahora hacemos otra matriz para corregir la perspectiva
        vertices_out = np.float32([
            # vértice superior izquierdo
            [punto_izquierda_arriba[0], punto_izquierda_arriba[1]],
            # vértice superior derecho ederezado al nivel de punto izquierda arriba
            [punto_derecha_arriba[0], punto_izquierda_arriba[1]],
            # vértice inferior derecho al nivel en "x" de la esq sup der y en "y" de la esq inf izq
            [punto_derecha_arriba[0], punto_izquierda_abajo[1]],
            #vértice inferior izuierdo al nivel en "x" del superior izquierdo
            [punto_izquierda_arriba[0], punto_izquierda_abajo[1]]
        ])
        #Obtengo la matriz de transformación con los vértices originales y los nuevos
        matriz_enderezar = cv.getPerspectiveTransform(vertices_in, vertices_out)
        #aplico la homografía
        imagen_transformada = cv.warpPerspective(imagen_original, matriz_enderezar, (imagen_original.shape[1], imagen_original.shape[0]))

#dibujo los círculos en los nuevos puntos del papel glasé
cv.circle(imagen_original,punto_izquierda_arriba,5,(255,0,0),-1)
cv.circle(imagen_original,(punto_izquierda_abajo[0],punto_izquierda_abajo[1]),5,(255,0,0),-1)
cv.circle(imagen_original,(punto_derecha_abajo[0],punto_derecha_abajo[1]),5,(255,0,0),-1)
cv.circle(imagen_original,punto_derecha_arriba,5,(255,0,0),-1)

#convierto la imágen sin perspectiva o enderezada a escala de grises
imagen_gris_transformada = cv.cvtColor(imagen_transformada, cv.COLOR_BGR2GRAY)
#aplico filtro gaussiano
imagen_gris_transformada = cv.GaussianBlur(imagen_gris_transformada, (5,5), 0)
#detecto lo bordes con canny
imagen_bordeada_transformada = cv.Canny(imagen_gris_transformada, 20, 180)
#aplico dilate y erode para mejorar los bordes
imagen_bordeada_transformada = cv.dilate(imagen_bordeada_transformada, None, iterations=1)
imagen_bordeada_transformada = cv.erode(imagen_bordeada_transformada, None, iterations=1)
#obtenemos los contornos cerrados nuevamente con la imagen enderezada
contornos_enderezados, hierarchy = cv.findContours(imagen_bordeada_transformada, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#recorremos todos los contornos de la imágen enderezada

for x,contorno in enumerate(contornos_enderezados):
    #print(cv.contourArea(contorno))
    #filtro áreas muy grande o muy chicas
    if x==4:
        continue
    #if cv.contourArea(contorno)==10.5:
    #    continue
    # copia = imagen_bordeada_transformada.copy()
    # obtengo un rectángulo con el área mínima del contorno
    box = cv.minAreaRect(contorno)
    # obtendo los puntos de ese rectágulo
    box = cv.boxPoints(box)
    # hago un numpy array entero con los punto del rectágulo
    box = np.array(box, dtype="int")
    # esta función lo que hace es ordenar los punto porque el rectágulo puede estar rotado
    # pero es opcional
    box = perspective.order_points(box)
    # ahora si, dibujamos las "cajas" alrededor de los contronos de las imágemes
    cv.drawContours(imagen_transformada, [box.astype("int")], -1, (0, 255, 0), 2)
    # ahora bien, cada "caja" contiene a su vez una tupla de 4 valores con los vértices de
    # dicha caja
    # entonces recorremos esos puntos con un for
    #esta condición es para áreas pequeñas, si no son grandes no sigue
    #con el if==indice del contorno actual que está recorriendo el for
    #encuentro la imágen que quiero medir,
    #el 0 es la goma
    #el 1 son las monedas juntas
    #el 2 es la tarjeta
    #el 3 es el papel glase
    if x==3:
        #puntos de los vértices de la "caja" del papel glasé
        (tlPG, trPG, brPG, blPG) = box
        #los imprimos para saber en que orden están
        #print(tlPG)
        #print(trPG)
        #print(brPG)
        #print(blPG)
        #obtengo la proporción restando las coordenadas en "X" de la arista superior
        proporcion = (trPG[0] - tlPG[0])
        #imprimo la proporción que es la longitud de la arista superior en píxeles que yo se que son 10cm
        #print(proporcion)

    if x==2:
        (tlT, trT, brT, blT) = box
        #print(tlT)
        #print(trT)
        #print(brT)
        #print(blT)
        alto_lado_izq = blT[1] - tlT[1]
        largo_borde_sup = trT[0] - tlT[0]
        #print(alto_lado_izq)
        #print(largo_borde_sup)

    if x==1:
        (tlM, trM, brM, blM) = box
        #print(tlM)
        #print(trM)
        #print(brM)
        #print(blM)
        alto_lado_moneda = blM[1] - tlM[1]
        largo_borde_moneda = trM[0] - tlM[0]

        largo_un_peso=largo_borde_moneda/2
        alto_50_centavos=alto_lado_moneda
        #diametro_moneda = tlM[1] - trM[1]
        #print(largo_borde_sup_moneda)
    if x==0:
        (tlG, trG, brG, blG) = box
        #print(tlG)
        #print(trG)
        #print(brG)
        #print(blG)
        alto_borde_goma = blG[1] - tlG[1]
        largo_borde_goma = trG[0] - tlG[0]


    for (x, y) in box:
        #dibujo un círculo en cada coordenada de cada vértice
        cv.circle(imagen_transformada, (int(x), int(y)), 5, (0, 0, 255), -1)
        #obtengo los vértice top_lef, top_righ, back_right y back_left
        (tl, tr, br, bl) = box
        #obtengo los puntos medios entre top_left y top_right o punto medio de la arista superior
        (tltrX, tltrY) = midpoint(tl, tr)
        #obtengo los puntos medios entre back_left y back_right o punto medio de la arista inferior
        (blbrX, blbrY) = midpoint(bl, br)
        #obtengo los puntos medios entre top_left y back_left o punto medio de la arista izquierda
        (tlblX, tlblY) = midpoint(tl, bl)
        # obtengo los puntos medios entre top_left y back_left o punto medio de la arista izquierda
        (trbrX, trbrY) = midpoint(tr, br)
        #dibujo un círculo en los puntos medios encontrados
        cv.circle(imagen_transformada, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
        cv.circle(imagen_transformada, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
        cv.circle(imagen_transformada, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
        cv.circle(imagen_transformada, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)
        #dibujo una línea entre los puntos medios
        cv.line(imagen_transformada, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),(255, 0, 255), 2)
        cv.line(imagen_transformada, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),(255, 0, 255), 2)

#hago la proporción respecto al papel glasé
alto_tarjeta = (alto_lado_izq * 10) / (proporcion)
ancho_tarjeta = (largo_borde_sup * 10) / (proporcion)
diametro_moneda_1peso=(largo_un_peso*10/proporcion)
diametro_moneda_50cent=(alto_50_centavos*10/proporcion)
alto_goma=(alto_borde_goma * 10) / (proporcion)
largo_goma=(largo_borde_goma * 10) / (proporcion)

#imprimo las medidas
#tarjeta
print('El alto de la tarjeta es:' , '{0:.3f}'.format(alto_tarjeta), ' cm aprox')
print('El ancho de la tarjeta es:' , '{0:.3f}'.format(ancho_tarjeta), ' cm aprox')
#moneda de 1 peso
print('El diametros de la moneda de 1 peso es:' , '{0:.3f}'.format(diametro_moneda_1peso), ' cm aprox')
#moneda de 50 centavos
print('El diametros de la moneda de 50 centavos es:' , '{0:.3f}'.format(diametro_moneda_50cent), ' cm aprox')
#medidas de la goma
print('El ancho de la goma es:' , '{0:.3f}'.format(largo_goma), ' cm aprox')
print('El alto de la goma es:' , '{0:.3f}'.format(alto_goma), ' cm aprox')

#while para mostrar las imágenes
while True:
    cv.imshow("practico10", imagen_original)
    k = cv.waitKey(20) & 0xFF
    #if k == ord('t'):
    cv.imshow("practico10win2", imagen_transformada)
    if k == ord('q'):
        break
cv.destroyAllWindows()
