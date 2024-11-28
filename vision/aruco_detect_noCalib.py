import cv2
import cv2.aruco as aruco
import glob
from aruco_dict import ARUCO_DICT

def detect_aruco_markers(image_path):
    """
    Detects ArUco markers in the given image and prints their IDs.

    Parameters:
        image_path (str): Path to the input image.

    Returns:
        None
    """
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read image from {image_path}.")
        return
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Define the ArUco dictionary
    aruco_dict = ARUCO_DICT["DICT_4X4_100"]
    
    # Initialize the detector parameters using default values
    parameters = aruco.DetectorParameters.create()
    
    # Detect the markers in the image
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    
    # If markers are detected
    if ids is not None:
        print(f"Detected {len(ids)} marker(s):")
        for marker_id in ids.flatten():
            print(f"Marker ID: {marker_id}")
            # Optionally, draw the marker boundaries and IDs on the image
            # aruco.drawDetectedMarkers(image, corners, ids)
            # cv2.putText(image, str(marker_id), (int(corners[0][0][0][0]), int(corners[0][0][0][1]) - 10),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    else:
        print("No ArUco markers detected.")
    
    # Display the image with detected markers (optional)
    # cv2.imshow('Detected ArUco markers', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    image_path = 'path_to_your_image.jpg'  # Replace with your image path
    detect_aruco_markers(image_path)