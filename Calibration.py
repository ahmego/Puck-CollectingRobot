import cv2 
import numpy as np 
def empty(val):
    pass
cv2.namedWindow("TrackBar")
cv2.resizeWindow("TrackBar",440,220)
cv2.createTrackbar("Hue Min","TrackBar",0,180,empty)
cv2.createTrackbar("Hue Max","TrackBar",180,180,empty)
cv2.createTrackbar("Sat Min","TrackBar",0,255,empty)
cv2.createTrackbar("Sat Max","TrackBar",255,255,empty)
cv2.createTrackbar("Val Min","TrackBar",0,255,empty)
cv2.createTrackbar("Val Max","TrackBar",255,255,empty)

def TrackBar(frame):
    H_Min=cv2.getTrackbarPos("Hue Min","TrackBar")
    H_Max=cv2.getTrackbarPos("Hue Max","TrackBar")
    S_Min=cv2.getTrackbarPos("Sat Min","TrackBar")
    S_Max=cv2.getTrackbarPos("Sat Max","TrackBar")
    V_Min=cv2.getTrackbarPos("Val Min","TrackBar")
    V_Max=cv2.getTrackbarPos("Val Max","TrackBar")
    LOwer=np.array([H_Min,S_Min,V_Min])
    UPper=np.array([H_Max,S_Max,V_Max])
    HSv_color=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    Mask=cv2.inRange(HSv_color,LOwer,UPper)
    cv2.imshow(" ",Mask)


Camera=cv2.VideoCapture(0)
while True:
    _,frame=Camera.read()
    # frameBlur=cv2.GaussianBlur(frame,(7,7),1)
    # frameGray=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)    
    # frameCanny=cv2.Canny(frameGray,70,150)
    TrackBar(frame)
    # cv2.imshow(" ",frameCanny)n 
    # cv2.imshow(" ",)
    
    if cv2.waitKey(0) & 0xFF == ord("q"):
        Camera.release()
        cv2.destroyAllWindows()
        break

