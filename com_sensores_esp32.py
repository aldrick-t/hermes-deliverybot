#!/usr/bin/env python3
import socket
import time
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port
from pybricks.ev3devices import InfraredSensor, ColorSensor

ev3 = EV3Brick()
ir_sensor = InfraredSensor(Port.S3)
color_sensor = ColorSensor(Port.S1)

#Establecer conexion con la esp32
esp32_address = 'E0:5A:1B:A0:CE:A6'  #Direccion MAC de la esp32 (YA NO CAMBIAR)
port = 1

sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
sock.connect((esp32_address, port))
print("Conectado al ESP32")

while True:

    infrared_distance = ir_sensor.distance()  #Tipo de dato INT
    reflected_light = color_sensor.reflection()  #Tipo de dato INT
    detected_color = color_sensor.color()  #Tipo de dato COLOR (ej. Color.red)

    #Mensaje a enviar
    message = f"IR Distance: {infrared_distance}, Light: {reflected_light}, Color: {detected_color}\n"
    
    #Envio de datos
    sock.send(message.encode())
    print("Datos enviados al ESP32:", message.strip())

    time.sleep(2) #tiempo de espera para volver a mandar los datos
