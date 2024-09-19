import numpy as np
import cv2
from matplotlib import pyplot as plt

cap = cv2. VideoCapture(0)

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap. get(4))
    
    #color conversion to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    #Color range selected to pale lime for testing
    # https://colorizer.org/ 
    lower_limit = np.array([78,20,20]) #blue range
    upper_limit = np.array([260,255,255])
    
    #mask to select the color range in the frame
    mask = cv2.inRange(hsv, lower_limit, upper_limit)
    
    #comprarator result, to show only the color range in the frame
    #blends image with bitwise_and then selects using mask
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    #laplasian filter
    laplasian = cv2.Laplacian(mask, cv2.CV_64F)
    laplasian = np.uint8(laplasian)
    cv2.imshow('laplasian', laplasian)
    
    #canny edge detection
    edges = cv2.Canny(mask, 100, 100)
    cv2.imshow('Canny', edges)
    
    #display the result frame and mask
    cv2.imshow('frame', result)
    cv2.imshow('mask', mask)
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows ()

#single pixel image conversion for color selection utility
# BGR_color = np.array[[[255,0,0]]]
# x = cv2.cvtColor(BGR_color, cv2.COLOR_BGR2HSV)
# x[0][0]
