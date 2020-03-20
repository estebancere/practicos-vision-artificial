import cv2
import sys

# if len(sys.argv) > 1:
#     filename = sys.argv[1]
# else:
#     print('Pass a file name as first argument')
#     sys.exit(0)

cap = cv2.VideoCapture('Activar_Office.wmv')

while cap.isOpened():
    ret, frame = cap.read()
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cv2.imshow('frame', gray)
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
print("Los FPS del video son: ", fps)
