import cv2
import HandTrackingModule as htm
import time
import socket, sys

cap = cv2.VideoCapture(0)
detector = htm.handDetector(detectconf=0.8)
lmlist = []
tipid = [4, 8, 12, 16, 20]

current_time = 0
previous_time = 0

prev_signal = '00'
def send_to_pi(message, s):
    global prev_signal
    if message=="Forward":
        signal = '1'
    elif message=="Reverse":
        signal = '2'
    elif message=="Right":
        signal = "3"
    elif message=="Left":
        signal = "4"
    else:
        signal = "0"
    if signal!=prev_signal:
        s.sendall(signal.encode('utf-8'))
        prev_signal = signal

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    try:
        s.connect(('192.168.0.103',12345))
    except:
        print("can't connect to rbpi")
        sys.exit(1)

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
                    send_to_pi('Stop', s)
                    cv2.putText(frame, 'Stop', (10, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=1, color=(255, 0, 255), thickness=3)
                #Forward Check
                elif fingerOpen == [1,1,0,0,1]:
                    send_to_pi('Forward', s)
                    cv2.putText(frame, 'Forward', (10, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=1, color=(255, 0, 255), thickness=3)
                #Reverse Check
                elif fingerOpen == [0,1,0,0,1]:
                    send_to_pi('Reverse', s)
                    cv2.putText(frame, 'Reverse', (10, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=1, color=(255, 0, 255), thickness=3)
                #Left Check
                elif fingerOpen == [1,0,0,0,1]:
                    send_to_pi('Left', s)
                    cv2.putText(frame, 'Left', (10, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=1, color=(255, 0, 255), thickness=3)
                #Right Check
                elif fingerOpen == [1,1,0,0,0]:
                    send_to_pi('Right', s)
                    cv2.putText(frame, 'Right', (10, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=1, color=(255, 0, 255), thickness=3)
                else:
                    #Stop Check 2
                    send_to_pi('Stop', s)
                    cv2.putText(frame, 'Stop', (10, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=1, color=(255, 0, 255), thickness=3)
            else:
                #No Hands Check/ Stop Check 3
                send_to_pi('No Hand Detected', s)
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
