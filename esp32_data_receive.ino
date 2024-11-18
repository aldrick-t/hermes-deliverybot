#include "BluetoothSerial.h"
BluetoothSerial SerialBT;

//Variables para almacenar los datos recibidos
int infraredDistance = 0;
int reflectedLight = 0;
String detectedColor = "";

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32_BT");
  Serial.println("El ESP32 está listo para comunicarse vía Bluetooth");
}

void loop() {
  //Revisar si hay datos entrantes desde el EV3
  if (SerialBT.available()) {
    String incomingData = SerialBT.readString(); // Lee los datos recibidos
    Serial.print("Datos recibidos desde EV3: ");
    Serial.println(incomingData);               // Muestra los datos en el monitor serie

    //Llamar a la funcion para que divida los datos
    decodeMessage(incomingData);
  }

  delay(100);
}

//Funcion para dividir los datos
void decodeMessage(String message) {
  if (message.startsWith("IR Distance:")) {
    int irIndex = message.indexOf(":") + 1;
    int lightIndex = message.indexOf("Light:");
    int colorIndex = message.indexOf("Color:");

    //Extraer los datos y regresarlos a su tipo correspondiente
    infraredDistance = message.substring(irIndex, lightIndex).toInt();
    reflectedLight = message.substring(lightIndex + 6, colorIndex).toInt();
    detectedColor = message.substring(colorIndex + 6).trim();

    //Imprimir en la terminal los datos recibidos
    Serial.println("Datos recibidos:");
    Serial.print("Distancia infrarroja: ");
    Serial.println(infraredDistance);
    Serial.print("Luz reflejada: ");
    Serial.println(reflectedLight);
    Serial.print("Color detectado: ");
    Serial.println(detectedColor);
  } else {
    Serial.println("Mensaje con formato no reconocido");
  }
}
