import cv

im = cv.LoadImage("/var/lib/cloud9/Dish-Detector/camera-test.jpg")

edges = cv.CreateImage(cv.GetSize(im), cv.IPL_DEPTH_8U, 1)

#convert the image to grayscale
cv.CvtColor(im, edges, cv.CV_BGR2GRAY)

#edge detect it, then smooth the edges
cv.Canny(edges, edges, 5, 300, 3)
cv.Smooth(edges, edges, cv.CV_GAUSSIAN, 5, 5)
cv.SaveImage("/var/lib/cloud9/Dish-Detector/camera-test-edges.jpg", edges)

#create storage for hough cirlces
storage = cv.CreateMat(640, 1, cv.CV_32FC3)

#find the circles, most of these parameters are magic numbers that work well enough for where the camera is installed
cv.HoughCircles(edges, storage, cv.CV_HOUGH_GRADIENT, 2, 50, 5, 300)

for i in range(storage.rows):
    val = storage[i, 0]
    radius = int(val[2])
    center = (int(val[0]), int(val[1]))
    print "circular feature at: " + str(center), "size: " , str(radius)
    cv.Circle(im, center, radius, (0, 255, 0), thickness=2) 

cv.SaveImage("/var/lib/cloud9/Dish-Detector/camera-test-circles.jpg", im)