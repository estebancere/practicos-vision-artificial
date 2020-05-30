import cv2
import numpy as np
#acá tuve que bajar porque no encontraba más de 9 matches
MIN_MATCH_COUNT = 9

##leo las imágenes
imagen1 = cv2.imread('aire1.jpeg')
imagen2 = cv2.imread('aire2.jpeg')

##las paso a escla de grises
#escuadra_der_gris=cv2.cvtColor(escuadra_der_orig,cv2.COLOR_BGR2GRAY)
#escuadra_izq_gris=cv2.cvtColor(escuadra_izq_orig,cv2.COLOR_BGR2GRAY)

#creo objeto SIFT
sift = cv2.xfeatures2d.SIFT_create()

#detecto puntos característicos y descriptores de la primera imagen
pts_caract_1, desc_1 = sift.detectAndCompute(imagen2, None)
#detecto puntos característicos y descriptores de la segunda imagen
pts_caract_2, desc_2 = sift.detectAndCompute(imagen1, None)

#dibujo los puntos caracteristicos en la imágen escuadra derecha
#cv2.drawKeypoints(imagen2, pts_caract_1, imagen2)
#dibujo los puntos caracteristicos en la imágen escuadra izquierda
#cv2.drawKeypoints(imagen1, pts_caract_2, imagen1)

#creo objeto de tipo matcher para encontrar la coincidencias
matcher = cv2.BFMatcher(cv2.NORM_L2)
matches = matcher.knnMatch(desc_1, desc_2, k=2)

# Guardamos los buenos matches usando el test de razón de Lowe
buenos_matches = []

for m,n in matches :
    if m.distance < 0.7*n.distance:
        buenos_matches.append(m)

if len(buenos_matches) > MIN_MATCH_COUNT:
    puntos_fuente=np.float32([pts_caract_1[m.queryIdx].pt for m in buenos_matches]).reshape(-1, 1, 2)
    puntos_destino = np.float32([pts_caract_2[m.trainIdx].pt for m in buenos_matches]).reshape(-1, 1, 2)
    # Computamos la homografía con RANSAC
    matriz,mask=cv2.findHomography(puntos_destino,puntos_fuente,cv2.RANSAC,5.0)

imagen_izq_transf=cv2.warpPerspective(imagen1, matriz, (imagen1.shape[1], imagen1.shape[0]))

# Mezclamos ambas imágenes
alpha = 0.5
blend = np.array(imagen_izq_transf * alpha + imagen2 * (1 - alpha), dtype=np.uint8)

#acá muestro
while True:
    cv2.imshow("practico12", blend)
    k = cv2.waitKey(20) & 0xFF
    if k == ord('q'):
        break
cv2.destroyAllWindows()