import cv

capture = cv.CaptureFromCAM(-1) #-1 will select the first camera available, usually /dev/video0 on linux
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 320)
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
im = cv.QueryFrame(capture)

cv.SaveImage("/var/lib/cloud9/Dish-Detector/sink-latest.jpg", im)

edges = cv.CreateImage(cv.GetSize(im), cv.IPL_DEPTH_8U, 1)

#convert the image to grayscale
cv.CvtColor(im, edges, cv.CV_BGR2GRAY)

#edge detect it, then smooth the edges
#cv.Canny(edges, edges, 5, 300, 3)
#cv.Smooth(edges, edges, cv.CV_GAUSSIAN, 5, 5)
thresh = 100
cv.Canny(edges, edges, thresh, thresh / 2, 3)
cv.Smooth(edges, edges, cv.CV_GAUSSIAN, 3, 3) 
cv.SaveImage("/var/lib/cloud9/Dish-Detector/sink-latest-edges.jpg", edges)

#create storage for hough cirlces
storage = cv.CreateMat(640, 1, cv.CV_32FC3)

#find the circles, most of these parameters are magic numbers that work well enough for where the camera is installed
#cv.HoughCircles(edges, storage, cv.CV_HOUGH_GRADIENT, 2, 50, 5, 300)
cv.HoughCircles(edges, storage, cv.CV_HOUGH_GRADIENT, 2, edges.width / 10, thresh, 350, 0, 0)

f = open("/var/lib/cloud9/Dish-Detector/sink-empty.txt", "r")
drains = []
for line in f:
    val = line.split(",")
    drains.append((int(val[0]), int(val[1]), int(val[2])))

tolerance = 8
for i in range(storage.rows):
    val = storage[i, 0]
    centerX = int(val[0])
    centerY = int(val[1])
    radius = int(val[2])
    isdrain = False
    for j in range(len(drains)):
        if abs(centerX - drains[j][0]) < tolerance:
            if abs(centerY - drains[j][1]) < tolerance:
                if abs(radius - drains[j][2]) < tolerance:
                        if drains[j][2] != 0:
                            isdrain = True
                            drains[j] = (drains[j][0], drains[j][1], 0)
    if isdrain:
        cv.Circle(im, (centerX, centerY), radius, (0, 255, 0), thickness=2) 
    else:
        print "circular feature at: " + str(centerX) + "," + str(centerY) + " size: " + str(radius)
        cv.Circle(im, (centerX, centerY), radius, (0, 0, 255), thickness=3) 

for j in range(len(drains)):
    if drains[j][2] != 0:
        print "drain not found at: " + str(drains[j][0]) + "," + str(drains[j][1])
        cv.Circle(im, (drains[j][0], drains[j][1]), 10, (255, 0, 0), thickness=3) 

cv.SaveImage("/var/lib/cloud9/Dish-Detector/sink-latest-circles.jpg", im)