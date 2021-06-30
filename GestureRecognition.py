import cv2
import HandTrackingModule as htm
import time


cap = cv2.VideoCapture(0)
detector = htm.handDetector(detectconf=0.8)
lmlist = []
tipid = [4, 8, 12, 16, 20]

current_time = 0
previous_time = 0
while True:
    retval, frame = cap.read()
    fingerOpen = []
    if retval == True:
        detector.findHands(frame, draw=True)
        lmlist = detector.findPosition(frame)
        frame = cv2.flip(frame, 1)
        if len(lmlist):
            for id in range(5):
                if id == 0:
                    if(lmlist[tipid[id]][1] < lmlist[tipid[id] - 2][1]):
                        fingerOpen.append(0)
                    else:
                        fingerOpen.append(1)
                else:
                    if(lmlist[tipid[id]][2] < lmlist[tipid[id] - 2][2]):
                        fingerOpen.append(1)
                    else:
                        fingerOpen.append(0)
            #Stop Check 1
            if fingerOpen == [0,0,0,0,0]:
                print('Stop')
                cv2.putText(frame, 'Stop', (10, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1, color=(255, 0, 255), thickness=3)
            #Forward Check
            elif fingerOpen == [1,1,0,0,1]:
                print('Forward')
                cv2.putText(frame, 'Forward', (10, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1, color=(255, 0, 255), thickness=3)
            #Reverse Check
            elif fingerOpen == [0,1,0,0,1]:
                print('Reverse')
                cv2.putText(frame, 'Reverse', (10, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1, color=(255, 0, 255), thickness=3)
            #Left Check
            elif fingerOpen == [1,0,0,0,1]:
                print('Left')
                cv2.putText(frame, 'Left', (10, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1, color=(255, 0, 255), thickness=3)
            #Right Check
            elif fingerOpen == [1,1,0,0,0]:
                print('Right')
                cv2.putText(frame, 'Right', (10, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1, color=(255, 0, 255), thickness=3)
            else:
                #Stop Check 2
                print('Stop')
                cv2.putText(frame, 'Stop', (10, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1, color=(255, 0, 255), thickness=3)
        else:
            #No Hands Check/ Stop Check 3
            print('No Hand Detected')
            cv2.putText(frame, 'No Hand', (10, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1, color=(255, 0, 255), thickness=3)
        current_time = time.time()
        fps = 1/(current_time - previous_time)
        previous_time = current_time
        cv2.putText(frame, 'FPS: {}'.format(str(int(fps))), (500, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1, color=(255, 0, 255), thickness=3)
        cv2.imshow('Window', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
