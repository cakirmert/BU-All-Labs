import serial
import canalystii
import csv
import struct
from datetime import datetime
import time
import ctypes
import msvcrt

# Connect to the Arduino via serial port
arduino_serial = serial.Serial('COM4', 9600)

# Connect to the Canalyst-II device
dev = canalystii.CanalystDevice(bitrate=500000)

# Function to send messages
def send_sensor_data_to_can(distance):
    # Convert distance to an integer by multiplying by 100
    distance_int = int(distance * 100)
    distance_bytes = distance_int.to_bytes(4, 'big')  # Convert distance to 4 bytes
    distance_data = (ctypes.c_ubyte * 8)(*distance_bytes, 0, 0, 0, 0)  # Ensure data is 8 bytes
    new_message = canalystii.Message(
        can_id=0x100,
        remote=False,
        extended=False,
        data_len=8,
        data=distance_data
    )
    
    # Send the message on CAN1
    dev.send(1, new_message)
    print(f"Sent: {new_message}")

# List to store the received messages
received_messages = []

try:
    print("Listening for CAN messages. Press 't' to transmit sensor data or 'q' to quit.")
    while True:
        # Listen for messages on CAN0
        msgs = dev.receive(0)
        for msg in msgs:
            print(f"Received: {msg}")
            received_messages.append({
                "can_id": msg.can_id,
                "data": list(msg.data),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })

        # Check for user keyboard input
        if msvcrt.kbhit():
            command = msvcrt.getch().decode('utf-8').strip()
            if command == 't':
                # Read the distance from the Arduino
                if arduino_serial.in_waiting > 0:
                    distance_str = arduino_serial.readline().decode('utf-8').strip()
                    distance = float(distance_str.replace(' cm', ''))
                    print(f"Distance: {distance} cm")
                    
                    # Send the distance to the CAN bus
                    send_sensor_data_to_can(distance)
            elif command == 'q':
                break
            
            # Delay for readability
            time.sleep(0.1)

except KeyboardInterrupt:
    print("Program interrupted. Exiting...")

finally:
    # Save the received messages to a CSV file
    with open("received_can_messages.csv", "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["can_id", "data", "timestamp", "ts_microseconds", "ts_milliseconds", "ts_seconds"])
        writer.writeheader()
        for msg in received_messages:
            writer.writerow(msg)

    # Stop both channels
    dev.stop(0)
    dev.stop(1)

    # Delete device to free the interface
    del dev
    
    # Close the serial connection
    arduino_serial.close()

print("Test completed and results saved to received_can_messages.csv")
