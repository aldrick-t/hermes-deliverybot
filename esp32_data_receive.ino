#include <WiFi.h>
#include <PubSubClient.h>
#include "BluetoothSerial.h"

BluetoothSerial SerialBT;

//Variables para almacenar los datos recibidos
int infraredDistance = 0;
int batteryPercentage = 0;
String boxStatus = "";

// Configuración WiFi y MQTT
const char* ssid = "steren_2_4G";
const char* password = "password";
const char* mqttServer = "192.168.1.36";
const int mqttPort = 1883;
const char* mqttUser = "";
const char* mqttPassword = "";

const char* mqttTopic_statusIn = "EV3/status_out";
String receivedStatus = "";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32_BT");
  Serial.println("El ESP32 está listo para comunicarse vía Bluetooth.");

  connectToWiFi();

  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
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

  //decodeMessage("data");
  //publishToMQTT();

  delay(100);
}

void callback(char* topic, byte* message, unsigned int length){
  
  receivedStatus = "";
  for (int i = 0; i < length; i++){
    receivedStatus += (char)message[i];
  }

  Serial.println(receivedStatus);
  SerialBT.println(receivedStatus);
}

// Función para decodificar el mensaje recibido
void decodeMessage(String message) {
  // Cortar los primeros 13 caracteres
  if (message.length() > 13) {
    message = message.substring(13);
    Serial.println(message);
  }

  // Comprobar si el mensaje tiene al menos tres 'A's para separar los datos
  int firstA = message.indexOf('A');
  int secondA = message.indexOf('A', firstA + 1);
  int thirdA = message.indexOf('A', secondA + 1);

  if (firstA != -1 && secondA != -1 && thirdA != -1) {
    // Extraer los datos basados en las posiciones de 'A'
    infraredDistance = message.substring(firstA + 1, secondA).toInt();
    batteryPercentage = message.substring(secondA + 1, thirdA).toInt();
    boxStatus = message.substring(thirdA + 1);

    // Imprimir los datos decodificados
    Serial.print("Distancia infrarroja: ");
    Serial.println(infraredDistance);
    Serial.print("Batería restante: ");
    Serial.println(batteryPercentage);
    Serial.print("Estado de la caja: ");
    Serial.println(boxStatus);
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
      client.subscribe(mqttTopic_statusIn);
    } else {
      Serial.print(".");
      delay(500);
    }
  }
}

// Publicacion de los datos en MQTT
void publishToMQTT() {
  Serial.println("se ha cambiado a seccion Publish2MQTT");
  String topicIR = "EV3/infrared";
  String topicBattery = "EV3/battery";
  String topicBox = "EV3/box_state";

  // Publicar cada dato en su tema correspondiente
  client.publish("EV3/infrared", String(infraredDistance).c_str());
  //Serial.println(infraredDistance);
  client.publish("EV3/battery", String(batteryPercentage).c_str());
  //Serial.println(batteryPercentage);
  client.publish("EV3/box_state", boxStatus.c_str());
  //Serial.println(boxStatus);

  Serial.println("Datos publicados en MQTT.");
}