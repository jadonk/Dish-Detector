import cv

capture = cv.CaptureFromCAM(-1) #-1 will select the first camera available, usually /dev/video0 on linux
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 320)
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
im = cv.QueryFrame(capture)
cv.SaveImage("/var/lib/cloud9/Dish-Detector/camera-test.jpg", im)