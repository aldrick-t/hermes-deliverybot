import cv2
import cv2.aruco as aruco
import urllib.request
import numpy as np
from aruco_dict import ARUCO_DICT

def detect_aruco_headless():
    """
    Detects ArUco markers in a live video stream from ESP32-CAM and prints their IDs without displaying the video.
    
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
    
    print("Starting headless ArUco marker detection from ESP32-CAM stream. Press 'Ctrl+C' to quit.")
    
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
                    
                    # Print detected marker IDs
                    if ids is not None:
                        for marker_id in ids.flatten():
                            print(f"Detected Marker ID: {marker_id}")
    except KeyboardInterrupt:
        print("Exiting headless marker detection.")
    finally:
        # Release resources if any
        pass

if __name__ == "__main__":
    detect_aruco_headless()