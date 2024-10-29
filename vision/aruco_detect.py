# ArUco Detection and Pose Estimation Module

import numpy as np
import cv2
from matplotlib import pyplot as plt
import cv2.aruco as aruco

def aruco_display(corners, ids, rejected, image):
    """
    Draws detected ArUco markers on the image and prints their IDs.

    Parameters:
        corners (list): Detected marker corners.
        ids (numpy.ndarray): Detected marker IDs.
        rejected (list): Rejected candidates.
        image (numpy.ndarray): The image on which to draw.

    Returns:
        image (numpy.ndarray): The image with drawn markers.
    """
    if len(corners) > 0:
        ids = ids.flatten()
        
        for (markerCorner, markerID) in zip(corners, ids):
            corners_reshaped = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners_reshaped
            
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))
            
            # Draw the bounding box of the ArUco marker
            cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
            
            # Calculate and draw the center of the marker
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
            
            # Draw the ArUco marker ID on the image
            cv2.putText(image, str(markerID), (topLeft[0], topLeft[1] - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Print the detected marker ID to the terminal
            print(f"[INFO] ArUco marker ID: {markerID}")
            
    return image

def pose_est(frame, aruco_dict_type, matrix_coeff, distortion_coeff, marker_length=0.02):
    """
    Detects ArUco markers in the given frame, estimates their pose, overlays the information on the frame,
    and prints marker information to the terminal when identification is confident.

    Parameters:
        frame (numpy.ndarray): The input image/frame where markers are to be detected.
        aruco_dict_type (int): The dictionary type from cv2.aruco (e.g., aruco.DICT_4X4_100).
        matrix_coeff (numpy.ndarray): The camera matrix obtained from calibration.
        distortion_coeff (numpy.ndarray): The distortion coefficients obtained from calibration.
        marker_length (float): The length of the marker's side in meters.

    Returns:
        annotated_frame (numpy.ndarray): The frame annotated with detected markers and pose information.
    """
    # Convert the frame to grayscale as ArUco detection requires grayscale images
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Initialize the ArUco dictionary and detector parameters
    aruco_dict = aruco.Dictionary_get(aruco_dict_type)
    parameters = aruco.DetectorParameters_create()
    
    # Detect ArUco markers in the image
    corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters=parameters,
                                                 cameraMatrix=matrix_coeff,
                                                 distCoeff=distortion_coeff)
    
    annotated_frame = frame.copy()
    
    if len(corners) > 0:
        # Draw detected markers on the image
        annotated_frame = aruco_display(corners, ids, rejected, annotated_frame)
        
        # Estimate the pose of each marker
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, marker_length, matrix_coeff, distortion_coeff)
        
        for i in range(len(ids)):
            # Draw the axis for each marker to visualize its orientation
            aruco.drawAxis(annotated_frame, matrix_coeff, distortion_coeff, rvecs[i], tvecs[i], marker_length * 0.5)
            
            # Optionally, print detailed pose information
            marker_id = ids[i][0]
            tvec = tvecs[i][0]
            rvec = rvecs[i][0]
            print(f"[INFO] Marker ID: {marker_id}")
            print(f"      Position (x, y, z): {tvec[0]:.2f}, {tvec[1]:.2f}, {tvec[2]:.2f}")
            # You can convert rvec to rotation matrix or Euler angles if needed

    return annotated_frame