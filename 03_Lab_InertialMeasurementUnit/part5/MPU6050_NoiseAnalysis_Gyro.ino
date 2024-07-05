#include <Wire.h>

#define MPU6050_ADDR 0x68
#define PWR_MGMT_1 0x6B
#define CONFIG 0x1A
#define GYRO_CONFIG 0x1B
#define GYRO_ZOUT_H 0x47

int16_t gz;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  mpu6050_init();
  Serial.println("MPU6050 initialized");
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    switch (command) {
      case '0':
        setDLPFMode(0); // Set bandwidth to 256Hz
        Serial.println("Set bandwidth to 256Hz");
        break;
      case '1':
        setDLPFMode(1); // Set bandwidth to 188Hz
        Serial.println("Set bandwidth to 188Hz");
        break;
      case '2':
        setDLPFMode(2); // Set bandwidth to 98Hz
        Serial.println("Set bandwidth to 98Hz");
        break;
      case '3':
        setDLPFMode(3); // Set bandwidth to 42Hz
        Serial.println("Set bandwidth to 42Hz");
        break;
      case '4':
        setDLPFMode(4); // Set bandwidth to 20Hz
        Serial.println("Set bandwidth to 20Hz");
        break;
      case '5':
        setDLPFMode(5); // Set bandwidth to 10Hz
        Serial.println("Set bandwidth to 10Hz");
        break;
      case '6':
        setDLPFMode(6); // Set bandwidth to 5Hz
        Serial.println("Set bandwidth to 5Hz");
        break;
      case 'M':
        send_batch_data(1000); // Send 1000 data points
        break;
    }
  }
  delay(10);
}

void mpu6050_init() {
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(PWR_MGMT_1);  // PWR_MGMT_1 register
  Wire.write(0x00);        // Set to 0 to wake up the MPU-6050
  Wire.endTransmission(true);

  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(GYRO_CONFIG); // GYRO_CONFIG register
  Wire.write(0x00);        // Set gyro full scale range to ±250deg/s
  Wire.endTransmission(true);

  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(CONFIG);      // CONFIG register
  Wire.write(0x00);        // Disable FSYNC, set DLPF to 260Hz
  Wire.endTransmission(true);
}

void setDLPFMode(uint8_t mode) {
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(CONFIG);  // CONFIG register
  Wire.write(mode);    // Set DLPF mode
  Wire.endTransmission(true);
}

void send_batch_data(int num_samples) {
  for (int i = 0; i < num_samples; i++) {
    read_gyro_data();
    Serial.println(gz);
    delay(10);  // Short delay to avoid overloading the serial buffer
  }
}

void read_gyro_data() {
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(GYRO_ZOUT_H);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU6050_ADDR, 2, true);

  gz = (Wire.read() << 8) | Wire.read();
}
