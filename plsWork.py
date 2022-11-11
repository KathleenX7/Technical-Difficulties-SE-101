from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np

#not sure what this is
def isset(v):
    try:
        type (eval(v))
    except:
        return 0
    else:
        return 1

#changes hsv values to rgb values
def nothing(x):
    pass

# cv2.namedWindow("Trackbars")
# cv2.createTrackbar("B", "Trackbars", 0, 255, nothing)
# cv2.createTrackbar("G", "Trackbars", 0, 255, nothing)
# cv2.createTrackbar("R", "Trackbars", 0, 255, nothing)

#initializes the camera object
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 30

#editing PiRGBArray
rawCapture = PiRGBArray(camera, size=(320,240))

#reading frames from camera module
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    #setting up color recognition
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # B = cv2.getTrackbarPos("B", "Trackbars")
    # G = cv2.getTrackbarPos("G", "Trackbars")
    # R = cv2.getTrackbarPos("R", "Trackbars")
    
    B = 0
    G = 255
    R = 0

    green = np.uint8([[[B,G,R]]])
    hsvGreen = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
    lowerLimit = np.uint8([hsvGreen[0][0][0]-10,100,100])
    upperLimit = np.uint8([hsvGreen[0][0][0]+10,255,255])

    #adjusting the threshold of the HSV image for range of selected color
    mask = cv2.inRange(hsv, lowerLimit, upperLimit)

    #actually taking out the objects of the colors in the frame
    result = cv2.bitwise_and(image, image, mask=mask)

    #///
    #start of contour finding, maybe test without this first
    
    #find contours in threshold (filtered) image
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__.split('.'))
    
    #findContours() has different form for opencv2 and opencv3 (includes boolean or not)
    if major_ver == "2" or major_ver == "3":
        _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    else:
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    #find contour with max area (most of that color, likely the object) and store it
    max_area = 0
    for cont in contours:
        area = cv2.contourArea(cont)
        if area > max_area:
            max_area = area
            best_cont = cont
    
    #find centroids of best_cont and draw a circle there
    if isset('best_cont'):
        M = cv2.moments(best_cont)
        cx, cy = int(M['m10'] / M['m00'], int(M['m01'] / M['m00']))
        cv2.circle(frame(cx, cy), 5, 255, -1)
        print("Central pos: (%d, %d)" % (cx, cy))
    else:
        print("[Warning]Tag lost...")
    
    #note that cx is the x position of the ping pong ball,
    #so drive motors until cx is equal/approximately at the 
    #center of the camera field
    #///
    
    # cv2.imshow("frame", image)
    # cv2.imshow("mask", mask)
    # cv2.imshow("result", result)
    key = cv2.waitKey(1)

    #clearing the stream
    rawCapture.truncate(0)
    if key == 27:
        break

# cv2.destroyAllWindows()
camera.close()