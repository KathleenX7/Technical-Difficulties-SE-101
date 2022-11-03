#import necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np

#changes hsv values to rgb values
def nothing(x):
    pass
cv2.namedWindow("Trackbars")
cv2.createTrackbar("B", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("G", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("R", "Trackbars", 0, 255, nothing)

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

#set pi camera parameters to optimize loading frames
#might need decrease resolution and increase framerate
width, height = 320, 240
camera = PiCamera
camera.resolution = (width, height)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(width, height))
time.sleep(1)

#reading frames
for frame in camera.capture_continous(rawCapture, format='bgr', use_video_port=True):
    image = frame.array
    frame = cv2.flip(image,1)