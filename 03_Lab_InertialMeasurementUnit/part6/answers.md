# 1. How does it work?
## The Arduino program reads data from the MPU-6050 sensor and sends it over the serial port to a connected computer running the Processing program. The MPU-6050 sensor provides accelerometer and gyroscope data, which the Arduino collects and transmits.

# 2. How do you find out the correction values that need to be entered into the program?
## Correction values or calibration values can be found by running the sensor in a stable environment and capturing the output over a period of time. The average of these values can be taken as the offset or bias. This bias can be subtracted from the actual readings to get the corrected values.