#!/usr/bin/env pybricks-micropython
from pybricks.parameters import Port, Color
from pybricks.ev3devices import ColorSensor, InfraredSensor, Motor
from pybricks.hubs import EV3Brick
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from pybricks.messaging import BluetoothMailboxClient, TextMailbox

# Inicializar EV3
ev3 = EV3Brick()

# Inicializar bluetooth
client = BluetoothMailboxClient()
mailbox = TextMailbox('msg', client)
client.connect('E0:5A:1B:A0:CE:A6')  # Dirección MAC de la ESP32 (NO CAMBIAR)

# Configuración de sensores y motores
left_motor = Motor(Port.A)
right_motor = Motor(Port.D)
servo_motor = Motor(Port.B)
color_sensor = ColorSensor(Port.S1)
infrared_sensor = InfraredSensor(Port.S3)
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# Constantes de control
BLACK = 0  # Reflexión medida en el fondo negro
WHITE = 10  # Reflexión medida en la línea blanca
THRESHOLD = (BLACK + WHITE) / 2  # Umbral para diferenciar negro de blanco
DRIVE_SPEED = 100
TURN_SPEED = 150  # Velocidad de giro al buscar la línea
PROPORTIONAL_GAIN = 1.2

# Constantes del sensor infrarrojo
STOP_DISTANCE = 20  # Distancia mínima para detener el robot (en cm)
WARNING_DISTANCE = 50  # Distancia para emitir alerta de proximidad

# Variables globales
battery_percentage = 0
box_state = "cerrado"

def follow_line():
    """Función para seguir la línea blanca."""
    reflection = color_sensor.reflection()

    if reflection > THRESHOLD:
        # Si detecta línea blanca, avanzar
        robot.drive(DRIVE_SPEED, 0)
    else:
        # Si no detecta línea, realizar un movimiento de búsqueda
        robot.stop()
        # Gira a la izquierda buscando
        robot.drive_time(0, -TURN_SPEED, 500)
        # Verifica si encontró la línea después de girar
        reflection = color_sensor.reflection()
        if reflection > THRESHOLD:
            return  # Si encuentra la línea, retoma el movimiento hacia adelante
        # Si no encontró, gira a la derecha
        robot.drive_time(0, TURN_SPEED, 1000)

def retrieve_battery():
    battery_voltage = ev3.battery.voltage()
    battery_voltage_volts = battery_voltage / 1000
    voltage_min = 6000  # Voltaje mínimo en milivoltios (6.0 V)
    voltage_max = 9000  # Voltaje máximo en milivoltios (9.0 V)
    battery_percentage = ((battery_voltage - voltage_min) / (voltage_max - voltage_min)) * 100
    battery_percentage = max(0, min(100, battery_percentage))  # Limitar entre 0% y 100%
    return battery_percentage

def handle_RED_station():
    """Acción al detectar una estación verde."""
    robot.stop()
    ev3.speaker.beep(1000, 300)  # Sonido de confirmación
    servo_motor.run_target(200, -45)  # Abrir la caja
    send_bluetooth_info("Abierto")
    wait(15000)  # Esperar 15 segundos
    servo_motor.run_target(200, 0)  # Cerrar la caja
    send_bluetooth_info("Cerrado")
    ev3.speaker.beep(500, 300)  # Sonido de finalización

def check_infrared():
    """Verifica la distancia constantemente y emite alertas."""
    distance = infrared_sensor.distance()
    if distance < STOP_DISTANCE:
        robot.stop()  # Detener el robot si está demasiado cerca
        ev3.speaker.beep(frequency=600, duration=200)  # Alerta de proximidad peligrosa
        return False  # No continuar hasta que el objeto esté más lejos
    elif distance < WARNING_DISTANCE:
        ev3.speaker.beep(frequency=400, duration=200)  # Alerta de proximidad media
    else:
        ev3.speaker.beep(frequency=200, duration=200)  # Alerta de proximidad lejana
    return True  # Permitir continuar

####################FUNCIONES BLUETOOTH##########################
def check_bluetooth_message():
    """Revisar mensajes enviados por Bluetooth."""
    response = mailbox.wait()
    if response:
        print("Datos recibidos desde ESP32:", response)
        if data == "DESTINO":
            handle_RED_station()

    wait(2000)  # Envía y recibe cada 2 segundos

def send_bluetooth_info(box_state):
    battery_percentage = retrieve_battery()
    infrared_distance = infrared_sensor.distance()  #Tipo de dato INT

    message = "\nA{}A{}A{}".format(infrared_distance, battery_percentage, box_state)
    mailbox.send(message)
    print("Datos enviados al ESP32:", message)
    wait(2000) #tiempo de espera para volver a mandar los datos

#################FIN FUNCIONES BLUETOOTH##########################

def main():
    """Bucle principal."""
    while True:
        # Verificar la distancia constantemente
        if not check_infrared():
            continue  # Si hay un objeto cerca, no seguir avanzando

        # Seguir la línea
        follow_line()

        #enviar datos BT
        send_bluetooth_info("Cerrado")
        #recibir datos BT
        #check_bluetooth_message()

        # Detectar color
        color = color_sensor.color()
        if color == Color.RED:
            handle_RED_station()  # Ejecutar acciones en estación verde

if __name__ == "__main__":
    main()