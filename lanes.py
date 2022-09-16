import platform
from string import hexdigits
import cv2
import numpy as np
import matplotlib.pyplot as plt


def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

# 4 steps in segmenting out the region of interest from the actual image
# 1. Prepare a black canvas
# 2. Make a np array of polygons' coordinates (comprising the highlighted region)
# 3. Shade the interested region with white (using fillPoly function) => mask ready
# 4. perform bitwise_and of mask and image


def region_of_interest(image):
    height = image.shape[0]
    # array of polygons, here we have only single polygon
    # polygons consist of the interested regions of image
    mask = np.zeros_like(image)  # step-1
    polygons = np.array(
        [[(200, height), (1100, height), (550, 250)]])  # step-2
    # fillPoly takes an array of polygons as input
    cv2.fillPoly(mask, polygons, 255)  # step-3
    masked_image = cv2.bitwise_and(image, mask)  # step-4
    return masked_image


def display_lines(lane_image, lines):
    line_image = np.zeros_like(lane_image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image


def make_coordinates(image, line_parameter):
    slope, intercept = line_parameter
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1, y1, x2, y2])


def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])


# image = cv2.imread("/Users/ajay/ML_Prac/Lane_Detection/test_image.jpeg")
# lane_image = np.copy(image)
# canny_image = canny(lane_image)
# cropped_image = region_of_interest(canny_image)
# lines = cv2.HoughLinesP(cropped_image, 1, np.pi/180, 100,
#                         np.array([]), minLineLength=40, maxLineGap=5)
# averaged_lines = average_slope_intercept(lane_image, lines)
# line_image = display_lines(lane_image, averaged_lines)
# combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)

# cv2.imshow("Result", combo_image)
# cv2.waitKey(0)

cap = cv2.VideoCapture("/Users/ajay/ML_Prac/Lane_Detection/test2.mp4")
while (cap.isOpened()):
    _, frame = cap.read()

    canny_image = canny(frame)

    cropped_image = region_of_interest(canny_image)

    lines = cv2.HoughLinesP(cropped_image, 1, np.pi/180, 100,
                            np.array([]), minLineLength=40, maxLineGap=5)
    averaged_lines = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, averaged_lines)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

    cv2.imshow("Result", combo_image)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
