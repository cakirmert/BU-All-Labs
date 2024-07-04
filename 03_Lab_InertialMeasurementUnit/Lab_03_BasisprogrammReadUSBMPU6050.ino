// Demoprogramm für Inertialsensor Cluster MPU6050
// Sensorik in der Mechatronik, Prof. Dr. Rasmus Rettig
// Connections: Arduino Nano: 5V-5V, GND-GND, A4-SDA ,A5-SCL
// Arduino Micro: 2-SDA, 3-SCL

#include <Wire.h>

#define sensor_address 0x68

void setup()
{
  // ggf. Übertragungsrate anpassen
  Serial.begin(9600);
  Wire.begin();
  delay(1000);
  
  // Powermanagement aufrufen
  // Sensor schlafen und Reset, Clock wird zunächst von Gyro-Achse Z verwendet 
  // Serial.println("Powermanagement aufrufen - Reset");
  SetConfiguration(0x6B, 0x80);
 
  // Kurz warten
  delay(500);
 
  // Powermanagement aufrufen
  // Sleep beenden und Clock von Gyroskopeachse X verwenden
  // Serial.println("Powermanagement aufrufen - Clock festlegen");
  SetConfiguration(0x6B, 0x03);
 
  delay(500);
 
  // Konfigruation  aufrufen
  // Default => Acc=260Hz, Delay=0ms, Gyro=256Hz, Delay=0.98ms, Fs=8kHz
  // Serial.println("Konfiguration aufrufen - Default Acc = 260Hz, Delay = 0ms");
  SetConfiguration(0x1A, 0x06);
  SetConfiguration(0x1B, 0x00);
  SetConfiguration(0x1C, 0x00);
   delay(500);

  // Leerzeichen
  //Serial.println("");
}

void loop()
{
  byte result[14];
  // Anfangs Adresse von Beschleunigungssensorachse X
  result[0] = 0x3B;
 
   // Aufruf des MPU6050 Sensor
  Wire.beginTransmission(sensor_address);
  // Anfangsadresse verwenden.
  Wire.write(result[0]);
  Wire.endTransmission();
  // 14 Bytes kommen als Antwort
  Wire.requestFrom(sensor_address, 14);
  // Bytes im Array ablegen
  for(int i = 0; i < 14; i++)
  {
    result[i] = Wire.read();
  }
 
  // Zwei Bytes ergeben eine Achsen Wert und könenn

// per Bit Shifting  zusammengelegt werden.
 
  // Beschleunigungssensor
  int acc_X = (((int)result[0]) << 8) | result[1];
  int acc_Y = (((int)result[2]) << 8) | result[3];
  int acc_Z = (((int)result[4]) << 8) | result[5];
 
  // Temperatur sensor
  int temp = (((int)result[6]) << 8) | result[7];
 
  // Gyroskopesensor
  int gyr_X = (((int)result[8]) << 8) | result[9];
  int gyr_Y = (((int)result[10]) << 8) | result[11];
  int gyr_Z = (((int)result[12]) << 8) | result[13];
 
  // Ausgabe
  // Serial.print("ACC X:\t");
  Serial.print(acc_X, DEC); Serial.print("\n");
  //Serial.print"Y:\t");
  // Serial.print(acc_Y); Serial.print("\t");
  //Serial.print("Z:\t");
  // Serial.print(acc_Z); Serial.print("\t");
  //Serial.print("Gyroskope X:\t");
  // Serial.print(gyr_X); 
  // Serial.print("\t");
  // Serial.print("Y:\t");
  // Serial.print(gyr_Y); Serial.print("\t");
  // Serial.print("Z:\t");
  // Serial.print(gyr_Z); Serial.print("\t\t");
 //Serial.print("Temperatur:\t");
 // Serial.print(temp); Serial.print("\n"); 
}

void SetConfiguration(byte reg, byte setting)
{
   // Aufruf des MPU6050 Sensor
  Wire.beginTransmission(sensor_address);
  // Register Aufruf
  Wire.write(reg);
  // Einstellungsbyte für das Register senden
  Wire.write(setting);
  Wire.endTransmission();
}
