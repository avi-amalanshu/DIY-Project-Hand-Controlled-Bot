import urllib.request
import cv2 as cv
import numpy as np
import imutils
import time
url = "http://192.168.0.218:8080/shot.jpg"
while True:
    imgpath = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(imgpath.read()), dtype = np.uint8)
    img = cv.imdecode(imgnp,-1)
    cv.imshow("w", img)
    if ord('q')==cv.waitKey(1):
        break
    time.sleep(1/20)
