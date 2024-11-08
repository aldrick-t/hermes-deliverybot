# DataLog de colores - v1.0
from pybricks.tools import DataLog, StopWatch
from pybricks.ev3devices import Motor

# Inicializar el DataLog y reloj
data_log = DataLog('time', 'color_detected')
watch = StopWatch()

def log_data(color):
    "Registra el tiempo y el color detectado."
    time = watch.time()
    data_log.log(time, color)

