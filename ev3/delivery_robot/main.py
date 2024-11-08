from line_follower import follow_line
from color_detection import detect_color
from infrared_sensor import alert_with_ir
from datalog import log_data
from mqtt_connection import connect_mqtt, receive_mqtt_message
from bluetooth_connection import connect_bluetooth, receive_bluetooth_message

def main():
    # Conectar MQTT y Bluetooth
    mqtt_client = connect_mqtt()
    bt_mailbox = connect_bluetooth()

    while True:
        # Lógica de seguimiento de línea
        follow_line()
        
        # Detección de colores y acciones
        detect_color()
        
        # Claxon con sensor infrarrojo
        alert_with_ir()
        
        # Registro de datos (se envía el color)
        log_data("color_detectado")

        # Comunicación MQTT y Bluetooth
        receive_mqtt_message(mqtt_client)
        receive_bluetooth_message(bt_mailbox)

if __name__ == "__main__":
    main()
