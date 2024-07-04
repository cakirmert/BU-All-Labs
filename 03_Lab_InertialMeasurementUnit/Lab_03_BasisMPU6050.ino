// Demo program for inertial measurement unit cluster MPU6050
// Lab for Bus systems and sensors, Prof. Dr. Rasmus Rettig
// Connections: Arduino Nano: 5V-5V, GND-GND, A4-SDA, A5-SCL
// Arduino Micro: 2-SDA, 3-SCL

#include <Wire.h>

#define sensor_address 0x68

void setup()
{
  // fit baudrate
  Serial.begin(9600);
  Wire.begin();
  delay(1000);
  
  // Powermanagement
  // sleep and reset sensor, use clock for Gyro Z axis 
  // Serial.println("Call Powermanagement - Reset");
  SetConfiguration(0x6B, 0x80);
 
  // wait
  delay(500);
 
  // Powermanagement
  // End sleep and use clock for GGyro X axis
  // Serial.println("Call Powermanagement - Set Clock");
  SetConfiguration(0x6B, 0x03);
 
  delay(500);
 
  // Configruation
  // Default => Acc=260Hz, Delay=0ms, Gyro=256Hz, Delay=0.98ms, Fs=8kHz
  // Serial.println("Call Configuration - Default Acc = 260Hz, Delay = 0ms");
  SetConfiguration(0x1A, 0x06);
  SetConfiguration(0x1B, 0x00);
  SetConfiguration(0x1C, 0x00);
  delay(500);


  //Serial.println("Setup finished\n");
}

void loop()
{
  byte result[14];
  // Start-address Acc-X
  result[0] = 0x3B;
 
   // Begin Communication with MPU6050 sensor
  Wire.beginTransmission(sensor_address);
  
  Wire.write(result[0]);	// Use start-address
  Wire.endTransmission();
  
  // Read 14 Bytes
  Wire.requestFrom(sensor_address, 14);
  
  // save Bytes in array
  for(int i = 0; i < 14; i++)
  {
    result[i] = Wire.read();
  }
 
  // Each axis value consists of two bytes.
  // Combine them by bitshifting: value = (byte_high << 8) | byte_low 
 
  // Acceleration sensor
  int acc_X = (((int)result[0]) << 8) | result[1];
  int acc_Y = (((int)result[2]) << 8) | result[3];
  int acc_Z = (((int)result[4]) << 8) | result[5];
 
  // Temperature sensor
  int temp = (((int)result[6]) << 8) | result[7];
 
  // Gyroscopesensor
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
  //Serial.print("Gyroskope X:\t");
  Serial.print(gyr_X); 
  Serial.print("\t");
  // Serial.print("Y:\t");
  Serial.print(gyr_Y); Serial.print("\t");
  // Serial.print("Z:\t");
  Serial.print(gyr_Z); Serial.print("\t\t");
 //Serial.print("Temperatur:\t");
 Serial.print(temp); Serial.print("\n"); 
}

void SetConfiguration(byte reg, byte setting)
{
   // Call MPU6050 Sensor
  Wire.beginTransmission(sensor_address);
  // Register Call
  Wire.write(reg);
  // Send configuration byte for the register
  Wire.write(setting);
  Wire.endTransmission();
}
