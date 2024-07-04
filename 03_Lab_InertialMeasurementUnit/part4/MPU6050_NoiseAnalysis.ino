#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;
int16_t ax, ay, az;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  mpu.initialize();
  if (mpu.testConnection()) {
    Serial.println("MPU6050 connection successful");
  } else {
    Serial.println("MPU6050 connection failed");
    while (1);
  }
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    switch (command) {
      case '0':
        mpu.setDLPFMode(MPU6050_DLPF_BW_256);
        Serial.println("Set bandwidth to 256Hz");
        break;
      case '1':
        mpu.setDLPFMode(MPU6050_DLPF_BW_188);
        Serial.println("Set bandwidth to 188Hz");
        break;
      case '2':
        mpu.setDLPFMode(MPU6050_DLPF_BW_98);
        Serial.println("Set bandwidth to 98Hz");
        break;
      case '3':
        mpu.setDLPFMode(MPU6050_DLPF_BW_42);
        Serial.println("Set bandwidth to 42Hz");
        break;
      case '4':
        mpu.setDLPFMode(MPU6050_DLPF_BW_20);
        Serial.println("Set bandwidth to 20Hz");
        break;
      case '5':
        mpu.setDLPFMode(MPU6050_DLPF_BW_10);
        Serial.println("Set bandwidth to 10Hz");
        break;
      case '6':
        mpu.setDLPFMode(MPU6050_DLPF_BW_5);
        Serial.println("Set bandwidth to 5Hz");
        break;
      case 'M':
        mpu.getAcceleration(&ax, &ay, &az);
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
