import cv2
import cv2.aruco as aruco
import glob
from aruco_dict import ARUCO_DICT

def detect_aruco_video():
    """
    Detects ArUco markers in a live video stream and prints their IDs.

    Returns:
        None
    """
    # Initialize video capture (0 for default camera)
    cap = cv2.VideoCapture(0)  # Replace with your video source if different
    
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return
    
    # Define the ArUco dictionary
    aruco_dict = aruco.getPredefinedDictionary(ARUCO_DICT["DICT_4X4_100"])
    
    # Initialize the detector parameters using default values
    parameters = cv2.aruco.DetectorParameters()
    
    print("Starting ArUco marker detection. Press 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect the markers in the image
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        
        # If markers are detected
        if ids is not None:
            for i, marker_id in enumerate(ids.flatten()):
                print(f"Detected Marker ID: {marker_id}")
                # Draw marker boundaries and IDs on the frame
                aruco.drawDetectedMarkers(frame, corners, ids)
                # Compute the center of the marker to place the text
                c = corners[i][0]
                center_x = int(c[:, 0].mean())
                center_y = int(c[:, 1].mean())
                cv2.putText(frame, str(marker_id), (center_x, center_y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Display the resulting frame
        cv2.imshow('ArUco Marker Detection', frame)
        
        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting marker detection.")
            break
    
    # Release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    detect_aruco_video()