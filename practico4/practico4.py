import cv2

cap=cv2.VideoCapture(0)
fps = int(cap.get(cv2.CAP_PROP_FPS))
height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
fourcc=cv2.VideoWriter_fourcc('X','V','I','D')
framesize=width,height
out=cv2.VideoWriter('output.avi',fourcc,fps,framesize)

while True:
    ret, frame=cap.read()
    if ret is True:
        out.write(frame)
        cv2.imshow('frame',frame)
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            break

cap.release()
out.release()
cv2.destroyAllWindows()
