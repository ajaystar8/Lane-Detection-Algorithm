import cv2
import numpy as np

# convert image to 3-color-channel numpy array
image = cv2.imread("/Users/ajay/ML_Prac/Lane_Detection/test_image.jpeg")

# work on this image. don't spoil original image
lane_image = np.copy(image)

# work on gray scale image as it has single color channel & hence has faster processing
gray = cv2.cvtColor(lane_image, cv2.COLOR_BGR2GRAY) 

# performing image noise filtering and smoothening of image using gaussian blur
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Canny edge detection
canny = cv2.Canny(blur, 50, 150)


# display image using the array form of image as inout arguement
cv2.imshow("Result", canny)
 
# image goes only when any key pressed
cv2.waitKey(0)
