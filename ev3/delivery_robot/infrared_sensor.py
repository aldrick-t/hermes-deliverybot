# Sección de código para el sensor infrarrojo v1.0
from pybricks.parameters import Port
from pybricks.ev3devices import InfraredSensor
from pybricks.hubs import EV3Brick

# Inicializar EV3 y el sensor infrarrojo
ev3 = EV3Brick()
infrared_sensor = InfraredSensor(Port.S3)

def alert_with_ir():
    """Genera un sonido como claxon según la proximidad detectada."""
    distance = infrared_sensor.distance()
    
    if distance < 20:
        frequency = 600   # Muy cerca
    elif distance < 50:
        frequency = 400   # Cerca
    else:
        frequency = 200   # Lejos
    
    ev3.speaker.beep(frequency=frequency, duration=200)
    wait(300)
