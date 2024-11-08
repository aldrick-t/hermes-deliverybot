# Seguidor de línea con reacción a bordes y estaciones v1.0
from pybricks.parameters import Color
from pybricks.tools import wait
from pybricks.ev3devices import ColorSensor, Motor
from pybricks.robotics import DriveBase

# Configuración de motores y sensor
left_motor = Motor(Port.A)
right_motor = Motor(Port.D)
color_sensor = ColorSensor(Port.S1)
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# Variables de control
BLACK = 9
WHITE = 85
THRESHOLD = (BLACK + WHITE) / 2
DRIVE_SPEED = 100
PROPORTIONAL_GAIN = 1.2

def follow_line():
    "Función para seguir una línea negra y reaccionar a los límites rojos."
    while True:
        # Calcular la desviación desde el umbral
        deviation = color_sensor.reflection() - THRESHOLD
        # Calcular la velocidad de giro
        turn_rate = PROPORTIONAL_GAIN * deviation
        # Controlar el robot
        robot.drive(DRIVE_SPEED, turn_rate)
        
        # Detectar color
        color = color_sensor.color()
        if color == Color.RED:
            # Borde detectado: retrocede o gira
            robot.drive(-DRIVE_SPEED, turn_rate)  # Retrocede
            wait(500)
        elif color == Color.GREEN:
            # Estación detectada: detente por 20 segundos
            robot.stop()
            wait(20000)

        # Esperar brevemente para la siguiente lectura
        wait(10)
