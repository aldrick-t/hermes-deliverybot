#opencv test for color detection and edge detection
import numpy as np
import cv2
from matplotlib import pyplot as plt

cap = cv2. VideoCapture(0)

def generate_aruco():
    # Define the dictionary we want to use
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

    # Generate a marker
    marker_id = 30
    marker_size = 200  # Size in pixels
    marker_image = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size)
    cv2.imwrite('marker_42.png', marker_image)
    plt.imshow(marker_image, cmap='gray', interpolation='nearest')
    plt.axis('off')  # Hide axes
    plt.title(f'ArUco Marker {marker_id}')
    plt.show()
    
def color_masking():
    #color conversion to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    #Color range selected to pale lime for testing
    # https://colorizer.org/ 
    lower_limit = np.array([90,20,20]) #blue range
    upper_limit = np.array([230,255,255])
    
    
    
    #mask to select the color range in the frame
    mask = cv2.inRange(hsv, lower_limit, upper_limit)
    
    #comprarator result, to show only the color range in the frame
    #blends image with bitwise_and then selects using mask
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    return result, mask

def edge_detection(result, mask):
    #laplasian filter
    laplasian = cv2.Laplacian(result, cv2.CV_64F)
    laplasian = np.uint8(laplasian)
    
    #canny edge detection
    edges = cv2.Canny(mask, 100, 100)
    
    return edges, laplasian

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap. get(4))
    
    result, mask = color_masking()
    
    edges, laplasian = edge_detection(result, mask)
    
    #display the result frame and mask
    cv2.imshow('frame', frame)
    cv2.imshow('blend', result)
    cv2.imshow('mask', mask)
    
    #display edge detection and filtering
    cv2.imshow('Canny', edges)
    cv2.imshow('laplasian', laplasian)
    
    
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows ()

#single pixel image conversion for color selection utility
# BGR_color = np.array[[[255,0,0]]]
# x = cv2.cvtColor(BGR_color, cv2.COLOR_BGR2HSV)
# x[0][0]
