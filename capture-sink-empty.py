import cv

capture = cv.CaptureFromCAM(-1) #-1 will select the first camera available, usually /dev/video0 on linux
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 320)
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
im = cv.QueryFrame(capture)

cv.SaveImage("/var/lib/cloud9/Dish-Detector/sink-empty.jpg", im)

edges = cv.CreateImage(cv.GetSize(im), cv.IPL_DEPTH_8U, 1)

#convert the image to grayscale
cv.CvtColor(im, edges, cv.CV_BGR2GRAY)

#edge detect it, then smooth the edges
#cv.Canny(edges, edges, 5, 300, 3)
#cv.Smooth(edges, edges, cv.CV_GAUSSIAN, 5, 5)
thresh = 100
cv.Canny(edges, edges, thresh, thresh / 2, 3)
cv.Smooth(edges, edges, cv.CV_GAUSSIAN, 3, 3) 
cv.SaveImage("/var/lib/cloud9/Dish-Detector/sink-empty-edges.jpg", edges)

#create storage for hough cirlces
storage = cv.CreateMat(640, 1, cv.CV_32FC3)

#find the circles, most of these parameters are magic numbers that work well enough for where the camera is installed
#cv.HoughCircles(edges, storage, cv.CV_HOUGH_GRADIENT, 2, 50, 5, 300)
cv.HoughCircles(edges, storage, cv.CV_HOUGH_GRADIENT, 2, edges.width / 10, thresh, 350, 0, 0)

f = open("/var/lib/cloud9/Dish-Detector/sink-empty.txt", "w")
for i in range(storage.rows):
    val = storage[i, 0]
    radius = int(val[2])
    center = (int(val[0]), int(val[1]))
    f.write(str(center[0]) + "," + str(center[1]) + "," + str(radius) + "\n")
    cv.Circle(im, center, radius, (0, 255, 0), thickness=2) 

cv.SaveImage("/var/lib/cloud9/Dish-Detector/sink-empty-circles.jpg", im)