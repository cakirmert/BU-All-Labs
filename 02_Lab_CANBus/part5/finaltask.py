import canalystii
import serial
import csv
from datetime import datetime

# Connect to the Canalyst-II device with specified bitrate
dev = canalystii.CanalystDevice(bitrate=500000)

# Setup serial communication for HC-SR04
ser = serial.Serial('COM3', 9600)
ser.flushInput()

# Function to read sensor data
def read_sensor_data():
    ser_bytes = ser.readline()
    return int(ser_bytes.decode("utf-8").strip())

# Function to send messages
def send_message(can_id, data):
    new_message = canalystii.Message(
        can_id=can_id,
        remote=False,
        extended=False,
        data_len=len(data),
        data=data
    )
    dev.send(1, new_message)
    print(f"Sent: {new_message}")

# Function to receive messages
def receive_messages(channel, num_messages=10):
    messages = []
    for _ in range(num_messages):
        msg = dev.receive(channel)
        if msg:
            print(f"Received: {msg[0]}")
            messages.append(msg[0])
    return messages

# Example function to handle CAN network communication
def can_network_communication():
    # Example data for each group (Replace this with actual data reading)
    group_data = {
        0x101: read_sensor_data,  # Group A's sensor data
        0x102: read_sensor_data,  # Group B's sensor data
        0x103: read_sensor_data   # Group C's sensor data
    }

    # Send messages for each group
    for can_id, read_data in group_data.items():
        sensor_data = read_data()
        pl = (sensor_data, 0, 0, 0, 0, 0, 0, 0)  # Adjust payload structure as needed
        send_message(can_id, pl)

    # Receive messages
    received_messages = receive_messages(1)

    # Log the results
    with open("can_network_results.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "CAN ID", "Data"])
        for msg in received_messages:
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg.can_id, msg.data])

# Run the CAN network communication
can_network_communication()

# Stop both channels and clean up
dev.stop(0)
dev.stop(1)
ser.close()
del dev

print("Network communication completed and results saved to can_network_results.csv")
