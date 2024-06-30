def HAND_COUNTER():
    import mediapipe as mp
    import cv2 
    import time
    time.sleep(2.0)
    mp_draw=mp.solutions.drawing_utils
    mp_hand=mp.solutions.hands
    tip_IDs=[4,8,12,16,20] 
    cap=cv2.VideoCapture(0)
    with mp_hand.Hands(min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        while True:
            _,frame=cap.read()
            cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            frame.flags.writeable=False
            result=hands.process(frame)
            frame.flags.writeable=True
            cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
            lmlist=[]
            if result.multi_hand_landmarks:
                for hand_landmark in result.multi_hand_landmarks:
                    MY_hands=result.multi_hand_landmarks[0]
                    for id,lm in enumerate(MY_hands.landmark):
                        h,w,c=frame.shape
                        cx,cy=int(lm.x*w),int(lm.y*h)
                        lmlist.append([id,cx,cy])
                    mp_draw.draw_landmarks(frame,hand_landmark,mp_hand.HAND_CONNECTIONS)
            fingers=[]        
            if len(lmlist)!=0:
                if lmlist[tip_IDs[0]][1] > lmlist[tip_IDs[0]-1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                for id in range(1,5):
                    if lmlist[tip_IDs[id]][2]<lmlist[tip_IDs[id]-2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                total=fingers.count(1)
            cv2.imshow("frame",frame)
            if cv2.waitKey(1)==ord("q"):
                cap.release()
                cv2.destroyAllWindows()
                return total