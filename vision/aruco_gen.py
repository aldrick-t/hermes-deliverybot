import numpy as np
import cv2
from matplotlib import pyplot as plt
from aruco_dict import ARUCO_DICT

def generate_aruco():
    # Define the dictionary we want to use
    aruco_dict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT["DICT_4X4_100"])

    # Generate a marker
    marker_id = 30
    marker_size = 400  # Size in pixels
    marker_image = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size)
    cv2.imwrite('marker_30.png', marker_image)
    plt.imshow(marker_image, cmap='gray', interpolation='nearest')
    plt.axis('off')  # Hide axes
    plt.title(f'ArUco Marker {marker_id}')
    plt.show()
    

generate_aruco()