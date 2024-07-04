import serial
import canalystii
import csv
from datetime import datetime
import time
import ctypes

# Connect to the Arduino via serial port
arduino_serial = serial.Serial('COM4', 9600)  # Replace 'COM4' with your Arduino's port

# Connect to the Canalyst-II device
dev = canalystii.CanalystDevice(bitrate=500000)

# Function to send and receive messages
def send_sensor_data_to_can(distance):
    # Convert distance to an integer by multiplying by 100
    distance_int = int(distance * 100)
    distance_bytes = distance_int.to_bytes(4, 'big')  # Convert distance to 2 bytes
    distance_data = (ctypes.c_ubyte * 8)(*distance_bytes, 0, 0, 0, 0)  # Ensure data is 8 bytes
    new_message = canalystii.Message(
        can_id=0x01,
        remote=False,
        extended=False,
        data_len=8,
        data=distance_data
    )
    
    # Send the message on CAN1
    dev.send(1, new_message)
    print(f"Sent: {new_message}")
    
    # Receive the message on CAN2
    received_message = dev.receive(0)
    print(f"Received: {received_message}")
    
    # Log the results
    results.append({
        "distance_cm": distance,
        "distance_int": distance_int,
        "sent_message": str(new_message),
        "received_message": str(received_message),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# List to store the results
results = []

try:
    while True:
        # Read the distance from the Arduino
        if arduino_serial.in_waiting > 0:
            distance_str = arduino_serial.readline().decode('utf-8').strip()
            distance = float(distance_str.replace(' cm', ''))
            print(f"Distance: {distance} cm")
            
            # Send the distance to the CAN bus
            send_sensor_data_to_can(distance)
            
            # Delay for readability
            time.sleep(1)

except KeyboardInterrupt:
    print("Program interrupted. Exiting...")

finally:
    # Save the results to a CSV file
    with open("sensor_can_results.csv", "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["distance_cm", "distance_int", "sent_message", "received_message", "timestamp"])
        writer.writeheader()
        for result in results:
            writer.writerow(result)

    # Stop both channels
    dev.stop(0)
    dev.stop(1)

    # Delete device to free the interface
    del dev
    
    # Close the serial connection
    arduino_serial.close()

print("Test completed and results saved to sensor_can_results.csv")
