# Versión: 1.0 - Conexion MQTT
import paho.mqtt.client as mqtt

# Configuración del cliente MQTT
BROKER_ADDRESS = "192.168.1.10"  # Cambia esta IP por la de tu broker MQTT
TOPIC = "robot/ev3"

def connect_mqtt():
    client = mqtt.Client()
    client.connect(BROKER_ADDRESS)
    return client

def send_mqtt_message(client, message):
    client.publish(TOPIC, message)

def receive_mqtt_message(client):
    client.loop_start()
    client.subscribe(TOPIC)

    # Aquí puedes agregar una función callback para procesar los mensajes
    def on_message(client, userdata, msg):
        print(f"Mensaje recibido: {msg.payload.decode()}")

    client.on_message = on_message
