// Demo program for Inertial Sensor Cluster MPU6050
// Sensing in Mechatronics, Prof. Dr. Rasmus Rettig
// Connections: Arduino Nano: 5V-5V, GND-GND, A4-SDA, A5-SCL
// Arduino Micro: 2-SDA, 3-SCL

#include <Wire.h>

#define sensor_address 0x68

void setup()
{
  // Adjust transmission rate if necessary
  Serial.begin(9600);
  Wire.begin();
  delay(1000);
  
  // Call power management
  // Put sensor to sleep and reset, clock initially used by gyro axis Z
  // Serial.println("Call power management - Reset");
  SetConfiguration(0x6B, 0x80);
 
  // Wait briefly
  delay(500);
 
  // Call power management
  // Wake up from sleep and use clock from gyro axis X
  // Serial.println("Call power management - Set clock");
  SetConfiguration(0x6B, 0x03);
 
  delay(500);
 
  // Call configuration
  // Default => Acc=260Hz, Delay=0ms, Gyro=256Hz, Delay=0.98ms, Fs=8kHz
  // Serial.println("Call configuration - Default Acc = 260Hz, Delay = 0ms");
  SetConfiguration(0x1A, 0x06);
  SetConfiguration(0x1B, 0x00);
  SetConfiguration(0x1C, 0x00);
  delay(500);

  // Empty line
  //Serial.println("");
}

void loop()
{
  byte result[14];
  // Starting address of acceleration sensor axis X
  result[0] = 0x3B;
 
  // Call the MPU6050 sensor
  Wire.beginTransmission(sensor_address);
  // Use starting address
  Wire.write(result[0]);
  Wire.endTransmission();
  // 14 bytes are received as response
  Wire.requestFrom(sensor_address, 14);
  // Store bytes in the array
  for(int i = 0; i < 14; i++)
  {
    result[i] = Wire.read();
  }
 
  // Two bytes make up one axis value and can be combined using bit shifting.
 
  // Acceleration sensor
  int acc_X = (((int)result[0]) << 8) | result[1];
  int acc_Y = (((int)result[2]) << 8) | result[3];
  int acc_Z = (((int)result[4]) << 8) | result[5];
 
  // Temperature sensor
  int temp = (((int)result[6]) << 8) | result[7];
 
  // Gyroscope sensor
  int gyr_X = (((int)result[8]) << 8) | result[9];
  int gyr_Y = (((int)result[10]) << 8) | result[11];
  int gyr_Z = (((int)result[12]) << 8) | result[13];
 
  // Output
  // Serial.print("ACC X:\t");
  Serial.print(acc_X, DEC); Serial.print("\t");
  //Serial.print"Y:\t");
  Serial.print(acc_Y); Serial.print("\t");
  //Serial.print("Z:\t");
  Serial.print(acc_Z); Serial.print("\t");
  //Serial.print("Gyroscope X:\t");
  Serial.print(gyr_X); 
  Serial.print("\t");
  // Serial.print("Y:\t");
  Serial.print(gyr_Y); Serial.print("\t");
  // Serial.print("Z:\t");
  Serial.print(gyr_Z); Serial.print("\t\t");
 //Serial.print("Temperature:\t");
 Serial.print(temp); Serial.print("\n"); 
}

void SetConfiguration(byte reg, byte setting)
{
   // Call the MPU6050 sensor
  Wire.beginTransmission(sensor_address);
  // Call the register
  Wire.write(reg);
  // Send the setting byte for the register
  Wire.write(setting);
  Wire.endTransmission();
}
