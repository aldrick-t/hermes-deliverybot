#!/usr/bin/env pybricks-micropython
from pybricks.parameters import Port, Color
from pybricks.ev3devices import ColorSensor, InfraredSensor, Motor
from pybricks.hubs import EV3Brick
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# Inicializar EV3
ev3 = EV3Brick()

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
TURN_SPEED = 50  # Velocidad de giro al buscar la línea
PROPORTIONAL_GAIN = 1.2

# Constantes del sensor infrarrojo
STOP_DISTANCE = 20  # Distancia mínima para detener el robot (en cm)
WARNING_DISTANCE = 50  # Distancia para emitir alerta de proximidad

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

def handle_RED_station():
    """Acción al detectar una estación verde."""
    robot.stop()
    ev3.speaker.beep(1000, 300)  # Sonido de confirmación
    servo_motor.run_target(200, -45)  # Abrir la caja
    wait(15000)  # Esperar 15 segundos
    servo_motor.run_target(200, 0)  # Cerrar la caja
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

def main():
    """Bucle principal."""
    while True:
        # Verificar la distancia constantemente
        if not check_infrared():
            continue  # Si hay un objeto cerca, no seguir avanzando

        # Seguir la línea
        follow_line()

        # Detectar color
        color = color_sensor.color()
        if color == Color.RED:
            handle_RED_station()  # Ejecutar acciones en estación verde

if __name__ == "__main__":
    main()
