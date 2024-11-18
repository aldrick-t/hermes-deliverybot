#include <WiFi.h>
#include <PubSubClient.h>
#include "BluetoothSerial.h"

BluetoothSerial SerialBT;

//Variables para almacenar los datos recibidos
int infraredDistance = 0;
int reflectedLight = 0;
String detectedColor = "";

// Configuración WiFi y MQTT
const char* ssid = "steren_2_4G";
const char* password = "password";
const char* mqttServer = "192.168.1.7";
const int mqttPort = 1883;
const char* mqttUser = "";
const char* mqttPassword = "";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32_BT");
  Serial.println("El ESP32 está listo para comunicarse vía Bluetooth.");

  connectToWiFi();

  client.setServer(mqttServer, mqttPort);
  connectToMQTT();
}

void loop() {
  if (SerialBT.available()) {
    String incomingData = SerialBT.readString(); //Recibir los datos
    Serial.print("Datos recibidos desde EV3: ");
    Serial.println(incomingData);               //Imprimir en terminal lo recibido

    //Decodificar el mensaje
    decodeMessage(incomingData);

    //mandar datos a MQTT
    publishToMQTT();
  }

  if (!client.connected()) {
    connectToMQTT();
  }
  client.loop();

  delay(100);
}

//Función para decodificar el mensaje recibido
void decodeMessage(String message) {
  if (message.startsWith("IR Distance:")) {
    int irIndex = message.indexOf(":") + 1;
    int lightIndex = message.indexOf("Light:");
    int colorIndex = message.indexOf("Color:");

    // Extraer y convertir los datos
    infraredDistance = message.substring(irIndex, lightIndex).toInt();
    reflectedLight = message.substring(lightIndex + 6, colorIndex).toInt();
    detectedColor = message.substring(colorIndex + 6).trim();

    // Imprimir los datos decodificados
    Serial.print("Distancia infrarroja: ");
    Serial.println(infraredDistance);
    Serial.print("Luz reflejada: ");
    Serial.println(reflectedLight);
    Serial.print("Color detectado: ");
    Serial.println(detectedColor);
  } else {
    Serial.println("Mensaje con formato no reconocido.");
  }
}

void connectToWiFi() {
  Serial.print("Conectando a WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConexión WiFi establecida.");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}

void connectToMQTT() {
  Serial.print("Conectando al broker MQTT...");
  while (!client.connected()) {
    if (client.connect("ESP32_Client", mqttUser, mqttPassword)) {
      Serial.println("\nConexión MQTT establecida.");
    } else {
      Serial.print(".");
      delay(500);
    }
  }
}

// Publicacion de los datos en MQTT
void publishToMQTT() {
  String topicIR = "EV3/infrared";
  String topicLight = "EV3/light";
  String topicColor = "EV3/color";

  // Publicar cada dato en su tema correspondiente
  client.publish(topicIR.c_str(), String(infraredDistance).c_str());
  client.publish(topicLight.c_str(), String(reflectedLight).c_str());
  client.publish(topicColor.c_str(), detectedColor.c_str());

  Serial.println("Datos publicados en MQTT.");
}

