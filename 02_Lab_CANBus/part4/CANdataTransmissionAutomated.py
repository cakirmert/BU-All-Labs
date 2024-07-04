import canalystii
import serial

# Setup serial communication for HC-SR04
ser = serial.Serial('COM3', 9600)
ser.flushInput()

# Connect to the Canalyst-II device with specified bitrate
dev = canalystii.CanalystDevice(bitrate=500000)

# Function to read sensor data
def read_sensor_data():
    ser_bytes = ser.readline()
    return int(ser_bytes[0:len(ser_bytes)-1].decode("utf-8"))

# Transmit and verify sensor data with error detection
total_messages = 100
errors = 0

for _ in range(total_messages):
    sensor_data = read_sensor_data()
    pl = (sensor_data, 0, 0, 0, 0, 0, 0, 0)
    new_message = canalystii.Message(
        can_id=0x3FE,
        remote=False,
        extended=False,
        data_len=8,
        data=pl
    )
    dev.send(1, new_message)
    print(f"Sent: {new_message}")

    received_message = dev.receive(1)[0]
    if received_message.data[0] != sensor_data:
        errors += 1
        print(f"Error: Sent {sensor_data}, Received {received_message.data[0]}")

# Print results
print(f"Total messages: {total_messages}, Errors: {errors}")

# Stop both channels and close serial connection
dev.stop(0)
dev.stop(1)
ser.close()
del dev
