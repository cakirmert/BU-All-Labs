#include <Wire.h>

#define sensor_address 0x68

void setup() {
  Serial.begin(115200); // Set baud rate to 115200
  Wire.begin();
  delay(1000);

  // Powermanagement
  SetConfiguration(0x6B, 0x80); // Reset sensor and put to sleep
  delay(500);
  SetConfiguration(0x6B, 0x03); // Wake up and set clock source
  delay(500);

  // Configuration
  SetConfiguration(0x1A, 0x06); // Configure DLPF
  SetConfiguration(0x1B, 0x00); // Configure Gyro
  SetConfiguration(0x1C, 0x00); // Configure Accel (default range ±2g)
  delay(500);
}

void loop() {
  if (Serial.available() > 0) { // Check if there is data available on the serial port
    char command = Serial.read(); // Read the incoming command
    switch (command) {
      case '0':
        SetConfiguration(0x1C, 0x00); // Set accelerometer range to ±2g
        Serial.println("Set range to ±2g");
        break;
      case '1':
        SetConfiguration(0x1C, 0x08); // Set accelerometer range to ±4g
        Serial.println("Set range to ±4g");
        break;
      case '2':
        SetConfiguration(0x1C, 0x10); // Set accelerometer range to ±8g
        Serial.println("Set range to ±8g");
        break;
      case '3':
        SetConfiguration(0x1C, 0x18); // Set accelerometer range to ±16g
        Serial.println("Set range to ±16g");
        break;
      case 'M':
        ReadAndPrintSensorData(); // Read and print sensor data
        break;
    }
  }
  delay(100); // Delay for 100 milliseconds
}

void SetConfiguration(byte reg, byte setting) {
  Wire.beginTransmission(sensor_address);
  Wire.write(reg);
  Wire.write(setting);
  Wire.endTransmission();
}

void ReadAndPrintSensorData() {
  byte result[14];
  result[0] = 0x3B;

  Wire.beginTransmission(sensor_address);
  Wire.write(result[0]);
  Wire.endTransmission();
  Wire.requestFrom(sensor_address, 14);
  for (int i = 0; i < 14; i++) {
    result[i] = Wire.read();
  }

  int acc_X = (((int)result[0]) << 8) | result[1];
  int acc_Y = (((int)result[2]) << 8) | result[3];
  int acc_Z = (((int)result[4]) << 8) | result[5];
  int gyr_X = (((int)result[8]) << 8) | result[9];
  int gyr_Y = (((int)result[10]) << 8) | result[11];
  int gyr_Z = (((int)result[12]) << 8) | result[13];

  Serial.print(acc_X); Serial.print(",");
  Serial.print(acc_Y); Serial.print(",");
  Serial.print(acc_Z); Serial.print(",");
  Serial.print(gyr_X); Serial.print(",");
  Serial.print(gyr_Y); Serial.print(",");
  Serial.println(gyr_Z);
}
