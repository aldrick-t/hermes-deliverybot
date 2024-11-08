# Version: 1.0 - Conexión Bluetooth
from pybricks.messaging import BluetoothMailboxClient, TextMailbox

def connect_bluetooth():
    client = BluetoothMailboxClient()
    client.connect("ESP32_CAM")  # Nombre de tu ESP32-CAM
    mailbox = TextMailbox("msg", client)
    return mailbox

def send_bluetooth_message(mailbox, message):
    mailbox.send(message)

def receive_bluetooth_message(mailbox):
    if mailbox.wait():
        return mailbox.read()
