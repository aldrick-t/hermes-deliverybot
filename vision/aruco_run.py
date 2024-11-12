import cv2
import cv2.aruco as aruco
import urllib.request
import numpy as np
from aruco_dict import ARUCO_DICT

def detect_aruco_video():
    """
    Detects ArUco markers in a live video stream from ESP32-CAM and prints their IDs.
    
    Returns:
        None
    """
    # Stream URL pointing to /stream endpoint
    stream_url = "http://192.168.4.1/stream"  # ESP32-CAM AP IP address with /stream endpoint
    
    # Open the stream using urllib
    stream = urllib.request.urlopen(stream_url)
    bytes_data = b''
    
    # Define the ArUco dictionary
    aruco_dict = aruco.getPredefinedDictionary(ARUCO_DICT["DICT_4X4_100"])
    
    # Initialize the detector parameters using default values
    parameters = aruco.DetectorParameters()
    
    print("Starting ArUco marker detection from ESP32-CAM stream. Press 'q' to quit.")
    
    try:
        while True:
            bytes_data += stream.read(1024)
            a = bytes_data.find(b'\xff\xd8')  # Start of JPEG
            b = bytes_data.find(b'\xff\xd9')  # End of JPEG
            if a != -1 and b != -1 and b > a:
                jpg = bytes_data[a:b+2]
                bytes_data = bytes_data[b+2:]
                
                # Decode JPEG to OpenCV frame
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                
                if frame is not None:
                    # Convert to grayscale
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    
                    # Detect ArUco markers
                    corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
                    
                    # Draw detected markers and print their IDs
                    if ids is not None:
                        aruco.drawDetectedMarkers(frame, corners, ids)
                        for i, marker_id in enumerate(ids.flatten()):
                            print(f"Detected Marker ID: {marker_id}")
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
    except KeyboardInterrupt:
        pass
    finally:
        # Release resources
        cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    detect_aruco_video()