import os
import numpy as np
import cv2
from matplotlib import pyplot as plt
from aruco_dict import ARUCO_DICT

def generate_aruco(marker_id):
    # Define the dictionary we want to use
    aruco_dict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT["DICT_4X4_100"])

    # Generate a marker
    marker_size = 400  # Size in pixels
    marker_image = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size)
    
    # Get the directory of the current script
    save_dir = os.path.dirname(__file__)
    
    # Define the save path within the vision folder
    save_path = os.path.join(save_dir, f'marker_{marker_id}.png')
    
    # Save the marker image to the specified path
    cv2.imwrite(save_path, marker_image)
    # plt.imshow(marker_image, cmap='gray', interpolation='nearest')
    # plt.axis('off')  # Hide axes
    # plt.title(f'ArUco Marker {marker_id}')
    # plt.show()


generate_aruco(30)
generate_aruco(60)
generate_aruco(90)
generate_aruco(33)
generate_aruco(96)