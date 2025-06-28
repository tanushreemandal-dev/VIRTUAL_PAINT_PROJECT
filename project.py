import cv2 
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Define BGR colors for drawing
myColorValues = [
    [255, 0, 0],   # Blue
    [0, 255, 0]    # Green
]

myPoints = []  # [x, y, colorId]
drawing_enabled = False  # Toggle with 'd'

def nothing(x):
    pass

# Trackbars for Blue
cv2.namedWindow("Blue Trackbars")
cv2.resizeWindow("Blue Trackbars", 300, 250)
cv2.createTrackbar("Hue Min", "Blue Trackbars", 99, 179, nothing)
cv2.createTrackbar("Hue Max", "Blue Trackbars", 179, 179, nothing)
cv2.createTrackbar("Sat Min", "Blue Trackbars", 228, 255, nothing)
cv2.createTrackbar("Sat Max", "Blue Trackbars", 255, 255, nothing)
cv2.createTrackbar("Val Min", "Blue Trackbars", 166, 255, nothing)
cv2.createTrackbar("Val Max", "Blue Trackbars", 255, 255, nothing)

# Trackbars for Green
cv2.namedWindow("Green Trackbars")
cv2.resizeWindow("Green Trackbars", 300, 250)
cv2.createTrackbar("Hue Min", "Green Trackbars", 35, 179, nothing)
cv2.createTrackbar("Hue Max", "Green Trackbars", 85, 179, nothing)
cv2.createTrackbar("Sat Min", "Green Trackbars", 100, 255, nothing)
cv2.createTrackbar("Sat Max", "Green Trackbars", 255, 255, nothing)
cv2.createTrackbar("Val Min", "Green Trackbars", 100, 255, nothing)
cv2.createTrackbar("Val Max", "Green Trackbars", 255, 255, nothing)

def findColor(img, colorId, lower, upper):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV, lower, upper)
    x, y = getContours(mask)
    if x != 0 and y != 0 and drawing_enabled:
        myPoints.append([x, y, colorId])
    return mask

def getContours(img):
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
            x, y, w, h = cv2.boundingRect(approx)
            return x + w // 2, y
    return 0, 0

def drawOnCanvas(points, colors):
    for point in points:
        cv2.circle(imgResult, (point[0], point[1]), 10, colors[point[2]], cv2.FILLED)

while True:
    success, img = cap.read()
    if not success:
        break

    imgResult = img.copy()

    # Read HSV values directly from trackbars (BLUE)
    b_h_min = cv2.getTrackbarPos("Hue Min", "Blue Trackbars")
    b_h_max = cv2.getTrackbarPos("Hue Max", "Blue Trackbars")
    b_s_min = cv2.getTrackbarPos("Sat Min", "Blue Trackbars")
    b_s_max = cv2.getTrackbarPos("Sat Max", "Blue Trackbars")
    b_v_min = cv2.getTrackbarPos("Val Min", "Blue Trackbars")
    b_v_max = cv2.getTrackbarPos("Val Max", "Blue Trackbars")
    lower_blue = np.array([b_h_min, b_s_min, b_v_min])
    upper_blue = np.array([b_h_max, b_s_max, b_v_max])

    # Read HSV values directly from trackbars (GREEN)
    g_h_min = cv2.getTrackbarPos("Hue Min", "Green Trackbars")
    g_h_max = cv2.getTrackbarPos("Hue Max", "Green Trackbars")
    g_s_min = cv2.getTrackbarPos("Sat Min", "Green Trackbars")
    g_s_max = cv2.getTrackbarPos("Sat Max", "Green Trackbars")
    g_v_min = cv2.getTrackbarPos("Val Min", "Green Trackbars")
    g_v_max = cv2.getTrackbarPos("Val Max", "Green Trackbars")
    lower_green = np.array([g_h_min, g_s_min, g_v_min])
    upper_green = np.array([g_h_max, g_s_max, g_v_max])

    # Detect blue (colorId = 0) and green (colorId = 1)
    mask_blue = findColor(img, 0, lower_blue, upper_blue)
    mask_green = findColor(img, 1, lower_green, upper_green)

    if drawing_enabled:
        drawOnCanvas(myPoints, myColorValues)

    # Show result and resized mask windows
    cv2.imshow("Result", imgResult)
    cv2.imshow("Blue Mask", cv2.resize(mask_blue, (300, 150)))
    cv2.imshow("Green Mask", cv2.resize(mask_green, (300, 150)))

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('d'):
        drawing_enabled = not drawing_enabled
        print("Drawing:", "ON" if drawing_enabled else "OFF")
