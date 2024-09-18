import numpy as np
import cv2

cap = cv2. VideoCapture (0)

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap. get(4))
    
    #color conversion to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    #Color range selected to pale lime for testing
    lower_lime = np.array([30,20,20])
    upper_lime = np.array([100,255,255])
    
    #mask to select the color range in the frame
    mask = cv2.inRange(hsv, lower_lime, upper_lime)
    
    #comprarator result, to show only the color range in the frame
    #blends image with bitwise_and then selects using mask
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    cv2.imshow('frame', result)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows ()

#single pixel image conversion for color selection utility
# BGR_color = np.array[[[255,0,0]]]
# x = cv2.cvtColor(BGR_color, cv2.COLOR_BGR2HSV)
# x[0][0]
