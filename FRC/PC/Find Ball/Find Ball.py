import numpy as np
import cv2 as cv

#########################################################################
#                                                                       #
#   THIS DOES NOT WORK ON JEVOIS, THIS RUNS ON THE COMPUTER INSTEAD     #
#                                                                       #
#########################################################################

cap = cv.VideoCapture(1)

# Change this stuff to change the mask that is used, if the color is in this range then it will be white (1), if it is not then it will be black (0)
# Color Boundries (H,S,V) out of 180, 255, 255 | Standard HSV is out of 360, 100%, 100%. OpenCV is weird.
Yellow_Lower = [20, 50, 100]
Yellow_Upper = [40, 220, 255]

lower = np.array(Yellow_Lower, dtype = "uint8")
upper = np.array(Yellow_Upper, dtype = "uint8")

while(True):
    # Capture frame-by-frame
    ret, src = cap.read()
    
    hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)

    # Our operations on the frame come here
    blur = cv.GaussianBlur(hsv, (3, 3), 0)

    mask = cv.inRange(hsv, lower, upper)

    #gray = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)

    canny_edge = cv.Canny(mask, 100, 200)

    #rows / 16
    rows = canny_edge.shape[0]
    circles = cv.HoughCircles(canny_edge, cv.HOUGH_GRADIENT, 1, 100,
                               param1=100, param2=20,
                               minRadius=5, maxRadius=75)
    

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv.circle(src, center, 1, (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            cv.circle(src, center, radius, (255, 0, 255), 3)

    cv.imshow("Detected Circles", src)
    cv.imshow("Mask", mask)
    cv.imshow("Canny Edge", canny_edge)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()