import cv2
import cv2.aruco as aruco
import urllib.request
import paho.mqtt.client as mqtt
import numpy as np
from aruco_dict import ARUCO_DICT

# MQTT Configuration
MQTT_SERVER = "192.168.1.36"
MQTT_PORT = 1883
MQTT_TOPIC_STATUS = "EV3/status"
MQTT_TOPIC_LOCATION = "EV3/location"


# Marker Mapping
MARKER_MAP = {
    31: {"name": "B4_Subway_31", "status": "STA_TRUE"},
    40: {"name": "Building_4", "status": "DEST_TRUE"},
    60: {"name": "Building_6", "status": "DEST_FALSE"}
}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
    else:
        print(f"Failed to connect, return code {rc}")

def publish_mqtt(client, status, name):
    client.publish(MQTT_TOPIC_STATUS, status)
    client.publish(MQTT_TOPIC_LOCATION, status)
    print(f"Published status: {status}")

def detect_aruco_headless():
    stream_url = "http://192.168.1.184/stream"
    stream = urllib.request.urlopen(stream_url)
    bytes_data = b''
    
    aruco_dict = aruco.getPredefinedDictionary(ARUCO_DICT["DICT_4X4_100"])
    parameters = aruco.DetectorParameters()
    
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.connect(MQTT_SERVER, MQTT_PORT, 60)
    mqtt_client.loop_start()
    
    print("Starting headless ArUco marker detection. Press 'Ctrl+C' to quit.")
    
    try:
        while True:
            bytes_data += stream.read(1024)
            a = bytes_data.find(b'\xff\xd8')
            b = bytes_data.find(b'\xff\xd9')
            if a != -1 and b != -1 and b > a:
                jpg = bytes_data[a:b+2]
                bytes_data = bytes_data[b+2:]
                
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                if frame is not None:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
                    
                    if ids is not None:
                        for marker_id in ids.flatten():
                            print(f"Detected Marker ID: {marker_id}")
                            if marker_id in MARKER_MAP:
                                status = MARKER_MAP[marker_id]["status"]
                                location = MARKER_MAP[marker_id]["name"]
                                publish_mqtt(mqtt_client, status, location)
                                print(f"Decision: {MARKER_MAP[marker_id]}")
    except KeyboardInterrupt:
        print("Exiting marker detection.")
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

if __name__ == "__main__":
    detect_aruco_headless()