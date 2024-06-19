import numpy as np 
import cv2
class CAMERA:
    def __init__(self,CamNumber):
        self.camera_Cap=cv2.VideoCapture(CamNumber)
        _,self.__frame__ = self.camera_Cap.read()
        self.center_x = self.__frame__.shape[1] // 2
        self.center_y = self.__frame__.shape[0] // 2 
    def Data_Reading(self):
        Data=open("Camera_Data.txt")
        return Data.readline()
    def ReadFrame(self):
        _,self.__frame__ = self.camera_Cap.read()
    def Hsv_Frame(self):
        return cv2.cvtColor(self.__frame__,cv2.COLOR_BGR2HSV)
    def Red_Blue_color(self):
        Mask=self.Hsv_Frame()
        Color_data=self.Data_Reading()
        if Color_data == ("red"):
            Lower_red=np.array([0,100,125])
            Upper_red=np.array([205,255,225])
            return cv2.inRange(Mask,Lower_red,Upper_red)
        elif Color_data == ("blue"):
            Lower_blue=np.array([90,95,60])
            Upper_blue=np.array([140,225,235])
            return cv2.inRange(Mask,Lower_blue,Upper_blue)
    def Distance_Center_Frame (self,cX_contour,cY_contour):
        Dis = []
        distance = np.sqrt((cX_contour - self.center_x) ** 2 + (cY_contour - self.center_y) ** 2)
        Dis.append(distance)
        min_distance = min(Dis)
        print("distance",min_distance)
        if(cX_contour>self.center_x):
            return ('+' + str(min_distance))
        else:
            return ('-' + str(min_distance))
    def Detect_Shape(self):
        Contour_Mask=self.Red_Blue_color()
        kernel=np.ones((5,5),'uint8')
        Mask_k=cv2.erode(Contour_Mask,kernel)
        contours,_=cv2.findContours(Mask_k,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for cnt in contours: 
            area=cv2.contourArea(cnt)
            approx=cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
            x=approx.ravel()[0]
            y=approx.ravel()[1]
            if 700<area:
                cv2.drawContours(self.__frame__,[approx],0,(0,255,0),3)
                if len(approx)==4:
                    cv2.putText(self.__frame__,"Rectangle",(x,y),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,0),cv2.LINE_4)
                elif 10<len(approx)<14:
                    cv2.putText(self.__frame__,"Circle",(x,y),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,0),cv2.LINE_4)
                    Mm=cv2.moments(cnt)     
                    if Mm['m00'] !=0 : 
                        cX=int(Mm['m10']/Mm['m00'])
                        cY=int(Mm['m01']/Mm['m00'])
                        dis=self.Distance_Center_Frame(cX,cY)
                        print(dis)
        cv2.imshow("Detect_shape",self.__frame__)
    def Color_Detection(self,frame):
        cv2.imshow("camera2",frame)
def Main():
    cam_obj = CAMERA(0)
    while True:
        cam_obj.ReadFrame()    
        cam_obj.Detect_Shape()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cam_obj.camera_Cap.release()
            cv2.destroyAllWindows()
            break
Main()