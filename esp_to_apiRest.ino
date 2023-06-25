#include <Wire.h>
#include <ESP8266WiFi.h>
#include <Arduino.h>
#include <ESPAsyncTCP.h>
#include <ESPAsyncWebServer.h>
//#include <MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Arduino_JSON.h>
#include <FS.h>
#include "MPU6050_6Axis_MotionApps612.h"



const char* ssid = "LAB INTELIGENCIA_RED PARA TODOS";
const char* password = "Lab inteligencia@3187088*";
//const char* ssid = "Progsistemas";
// char* password = "ingsisMAY23";

//---------------------------added-----------------------------------------
const int S0 = 2;
const int S1 = 14;
const int S2 = 12;
const int S3 = 13;

const int in = 0;



// Create a sensor object
MPU6050 mpu;

int16_t gXHD, gYHD, gZHD;
int16_t aXHD, aYHD, aZHD;

int16_t gXCOD, gYCOD, gZCOD;
int16_t aXCOD, aYCOD, aZCOD;

int16_t gXMD, gYMD, gZMD;
int16_t aXMD, aYMD, aZMD;


//*****************************************************************
//********BRAZO DERECHO*******
//giroscopio 1 conectado a C2 - HOMBRO
void out1() {
  //c2
  digitalWrite(S0, LOW);    //0
  digitalWrite(S1, HIGH);   //1
  digitalWrite(S2, LOW);    //0
  digitalWrite(S3, LOW);    //0
  //0010 = pin c2 del multiplexor
}

//giroscopio 2 conectado a C3 - CODO
void out2() {
  //c3
  digitalWrite(S0, HIGH);  //1
  digitalWrite(S1, HIGH);  //1
  digitalWrite(S2, LOW);   //0
  digitalWrite(S3, LOW);   //0

  //0011 = pin c3 del multiplexor
}

//giroscopio 3 conectado a C4 - MUÑECA
void out3() {
  //c4
  digitalWrite(S0, LOW);   //0
  digitalWrite(S1, LOW);   //0
  digitalWrite(S2, HIGH);  //1
  digitalWrite(S3, LOW);   //0

  //0100 = pin c4 del multiplexor
}


// Init MPU6050
void initMPU() {
  out1();
  out2();
  out3();
  //out1();
  Wire.begin();           //Iniciando I2C
  mpu.initialize();    //Iniciando el sensor

  if (mpu.testConnection()) Serial.println("Sensor iniciado correctamente");
  else Serial.println("Error al iniciar el sensor");
}



//HOMBRO DERECHO
String getGyroAndAccHD() {
  out1();
  mpu.getRotation(&gXHD, &gYHD, &gZHD);
   mpu.getAcceleration(&aXHD, &aYHD, &aZHD);
// Json Variable to Hold Sensor Readings
JSONVar readings;
  readings["gXHD"] = String(gXHD);
  readings["gYHD"] = String(gYHD);
  readings["gZHD"] = String(gZHD);

  // Get current acceleration values
  aXHD = aXHD;
  aYHD = aYHD;
  aZHD = aZHD;
  readings["aXHD"] = String(aXHD);
  readings["aYHD"] = String(aYHD);
  readings["aZHD"] = String(aZHD);

  String accString = JSON.stringify (readings);
  return accString;
}


//CODO DERECHO
String getGyroAndAccCOD() {
  out2();
  mpu.getRotation(&gXCOD, &gYCOD, &gZCOD);
    mpu.getAcceleration(&aXCOD, &aYCOD, &aZCOD);
// Json Variable to Hold Sensor Readings
JSONVar readings;
  readings["gXCOD"] = String(gXCOD);
  readings["gYCOD"] = String(gYCOD);
  readings["gZCOD"] = String(gZCOD);


  aXCOD = aXCOD;
  aYCOD = aYCOD;
  aZCOD = aZCOD;
  readings["aXCOD"] = String(aXCOD);
  readings["aYCOD"] = String(aYCOD);
  readings["aZCOD"] = String(aZCOD);

  String accString = JSON.stringify (readings);
  return accString;
}

//MUÑECA DERECHA
String getGyroAndAccMD() {
  out3();
  mpu.getRotation(&gXMD, &gYMD, &gZMD);
    mpu.getAcceleration(&aXMD, &aYMD, &aZMD);
// Json Variable to Hold Sensor Readings
JSONVar readings;
  readings["gXMD"] = String(gXMD);
  readings["gYMD"] = String(gYMD);
  readings["gZMD"] = String(gZMD);



  aXMD = aXMD;
  aYMD = aYMD;
  aZMD = aZMD;
  readings["aXMD"] = String(aXMD);
  readings["aYMD"] = String(aYMD);
  readings["aZMD"] = String(aZMD);

  String accString = JSON.stringify (readings);
  return accString;
}
//-------------------------------------------------------------------

WiFiServer server(80);

void setup() {
///-------------------added------------------------------
    //declaramos los pines que están conectados al MUX como salida
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);

  
  //declaramos el pin conectado a int como salida
  pinMode(in, OUTPUT);

  //declaramos el pin conectado a int como bajo
  digitalWrite(in, LOW);  //0
    initMPU();
  ///----------------------------------------------------------------------------------------
  Wire.begin(4, 5);  // Pines SDA y SCL del ESP8266 (D1 y D2)


  Serial.begin(9600);
  delay(10);

  //Configuración  del GPIO2
  pinMode(2, OUTPUT);
  digitalWrite(2, LOW);


  Serial.println();
  Serial.println();
  Serial.print("Conectandose a red : ");
  Serial.println(ssid);

  WiFi.begin(ssid, password); //Conexión a la red

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi conectado");


  server.begin(); //Iniciamos el servidor
  Serial.println("Servidor Iniciado");


  Serial.println("Ingrese desde un navegador web usando la siguiente IP:");
  Serial.println(WiFi.localIP()); //Obtenemos la IP



  // Inicializar los sensores

}

void loop() {

  WiFiClient client = server.available();
  if (client){ //Si hay un cliente presente
  //Serial.print("SENSOR 1\n");
  String sensor1= getGyroAndAccHD();
  //Serial.print("SENSOR 2\n");
  String sensor2= getGyroAndAccCOD();
  //Serial.print("SENSOR 3\n");
  String sensor3= getGyroAndAccMD();
  String totalJson="["+sensor1+","+sensor2+","+sensor3+"]";

    Serial.println("Nuevo Cliente");

    //esperamos hasta que hayan datos disponibles
    while (!client.available() && client.connected())
    {
      delay(1);
    }

    // Leemos la primera línea de la petición del cliente.
    String linea1 = client.readStringUntil('r');
    Serial.println(linea1);


    client.flush();

    Serial.println("Enviando respuesta...");
    //Encabesado http
    client.println("HTTP/1.1 200 OK");
client.println("Content-Type: application/json");

    client.println("Connection: close");// La conexión se cierra después de finalizar de la respuesta
    client.println();
    //Pagina html  para en el navegador
    client.println(totalJson);

    delay(100);
    Serial.println("respuesta enviada");
    Serial.println();

  }
}
