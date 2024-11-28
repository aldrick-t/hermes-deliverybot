import cv2
import numpy as np
import cv2.aruco as aruco

# Import your ArUco detection functions
from vision.aruco_detect_poseEst import pose_est 

# Load calibration data
def load_calibration_data(filename):
    data = np.load(filename)
    camera_matrix = data['camera_matrix']
    distortion_coeff = data['distortion_coeff']
    return camera_matrix, distortion_coeff

matrix_coeff, distortion_coeff = load_calibration_data('calibration_data.npz')

# Define the ArUco dictionary to use
aruco_dict_type = aruco.DICT_4X4_100

# Initialize video capture (0 for default camera)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Perform ArUco detection and pose estimation
    annotated_frame = pose_est(frame, aruco_dict_type, matrix_coeff, distortion_coeff, marker_length=0.05)  # marker_length in meters

    # Display the resulting frame
    cv2.imshow('ArUco Detection', annotated_frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()