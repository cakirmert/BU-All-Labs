#include <Wire.h>

#define MPU6050_ADDR 0x68
#define PWR_MGMT_1 0x6B
#define SMPLRT_DIV 0x19
#define CONFIG 0x1A
#define GYRO_CONFIG 0x1B
#define ACCEL_CONFIG 0x1C
#define ACCEL_XOUT_H 0x3B

int16_t ax, ay, az;

void setup() {
  Serial.begin(9600);
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
        read_accel_data();
        Serial.print(ax);
        Serial.print(",");
        Serial.print(ay);
        Serial.print(",");
        Serial.println(az);
        break;
    }
  }
  delay(100);
}

void mpu6050_init() {
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(PWR_MGMT_1);  // PWR_MGMT_1 register
  Wire.write(0x00);        // Set to 0 to wake up the MPU-6050
  Wire.endTransmission(true);

  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(SMPLRT_DIV);  // SMPLRT_DIV register
  Wire.write(0x07);        // Set sample rate to 1kHz
  Wire.endTransmission(true);

  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(CONFIG);      // CONFIG register
  Wire.write(0x00);        // Disable FSYNC, set DLPF to 260Hz
  Wire.endTransmission(true);

  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(GYRO_CONFIG); // GYRO_CONFIG register
  Wire.write(0x00);        // Set gyro full scale range to ±250deg/s
  Wire.endTransmission(true);

  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(ACCEL_CONFIG);// ACCEL_CONFIG register
  Wire.write(0x00);        // Set accelerometer full scale range to ±2g
  Wire.endTransmission(true);
}

void setDLPFMode(uint8_t mode) {
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(CONFIG);  // CONFIG register
  Wire.write(mode);    // Set DLPF mode
  Wire.endTransmission(true);
}

void read_accel_data() {
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(ACCEL_XOUT_H);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU6050_ADDR, 6, true);

  ax = (Wire.read() << 8) | Wire.read();
  ay = (Wire.read() << 8) | Wire.read();
  az = (Wire.read() << 8) | Wire.read();
}
