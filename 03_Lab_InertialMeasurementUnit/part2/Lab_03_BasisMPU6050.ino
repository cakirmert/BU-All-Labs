#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu; // Create an instance of the MPU6050 class
int16_t ax, ay, az; // Variables to store accelerometer data
int16_t gx, gy, gz; // Variables to store gyroscope data
char buffer[10]; // Buffer for serial communication

void setup() {
  Serial.begin(9600); // Initialize serial communication
  Wire.begin(); // Initialize I2C communication
  mpu.initialize(); // Initialize the MPU6050
  if (mpu.testConnection()) { // Check if the MPU6050 is connected
    Serial.println("MPU6050 connection successful"); // Print success message
  } else {
    Serial.println("MPU6050 connection failed"); // Print failure message
    while (1); // Loop indefinitely if connection fails
  }
}

void loop() {
  if (Serial.available() > 0) { // Check if there is data available on the serial port
    char command = Serial.read(); // Read the incoming command
    switch (command) {
      case '0':
        mpu.setFullScaleAccelRange(MPU6050_ACCEL_FS_2); // Set accelerometer range to ±2g
        Serial.println("Set range to ±2g"); // Print message
        break;
      case '1':
        mpu.setFullScaleAccelRange(MPU6050_ACCEL_FS_4); // Set accelerometer range to ±4g
        Serial.println("Set range to ±4g"); // Print message
        break;
      case '2':
        mpu.setFullScaleAccelRange(MPU6050_ACCEL_FS_8); // Set accelerometer range to ±8g
        Serial.println("Set range to ±8g"); // Print message
        break;
      case '3':
        mpu.setFullScaleAccelRange(MPU6050_ACCEL_FS_16); // Set accelerometer range to ±16g
        Serial.println("Set range to ±16g"); // Print message
        break;
      case 'M':
        mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz); // Get motion data from the MPU6050
        Serial.print(ax); Serial.print(","); // Print accelerometer data
        Serial.print(ay); Serial.print(",");
        Serial.print(az); Serial.print(",");
        Serial.print(gx); Serial.print(","); // Print gyroscope data
        Serial.print(gy); Serial.print(",");
        Serial.println(gz);
        break;
    }
  }
  delay(100); // Delay for 100 milliseconds
}
