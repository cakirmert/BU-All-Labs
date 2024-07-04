import serial
import canalystii
import csv
import struct
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
    distance_bytes = distance_int.to_bytes(4, 'big')  # Convert distance to 4 bytes
    distance_data = (ctypes.c_ubyte * 8)(*distance_bytes, 0, 0, 0, 0)  # Ensure data is 8 bytes
    new_message = canalystii.Message(
        can_id=0x100,  # Example CAN ID
        remote=False,
        extended=False,
        data_len=8,
        data=distance_data
    )
    
    # Send the message on CAN1
    dev.send(1, new_message)
    print(f"Sent: {new_message}")
    
    # Receive the message on CAN2
    received_messages = dev.receive(0)
    for received_message in received_messages:
        print(f"Received: {received_message}")
        
        # Check for errors
        sent_data = new_message.data[:new_message.data_len]
        received_data = received_message.data[:received_message.data_len]
        if sent_data != received_data:
            errors.append({
                "distance_cm": distance,
                "sent_message": str(new_message),
                "received_message": str(received_message),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

# List to store the results
results = []
errors = []

try:
    count = 0
    while count < 100:
        # Read the distance from the Arduino
        if arduino_serial.in_waiting > 0:
            distance_str = arduino_serial.readline().decode('utf-8').strip()
            distance = float(distance_str.replace(' cm', ''))
            print(f"Distance: {distance} cm")
            
            # Send the distance to the CAN bus
            send_sensor_data_to_can(distance)
            count += 1
            
            # Log the results
            results.append({
                "distance_cm": distance,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # Delay for readability
            time.sleep(0.1)

except KeyboardInterrupt:
    print("Program interrupted. Exiting...")

finally:
    # Save the results to a CSV file
    with open("sensor_can_results.csv", "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["distance_cm", "timestamp"])
        writer.writeheader()
        for result in results:
            writer.writerow(result)

    # Save the errors to a CSV file
    with open("sensor_can_errors.csv", "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["distance_cm", "sent_message", "received_message", "timestamp"])
        writer.writeheader()
        for error in errors:
            writer.writerow(error)

    # Stop both channels
    dev.stop(0)
    dev.stop(1)

    # Delete device to free the interface
    del dev
    
    # Close the serial connection
    arduino_serial.close()

# Summary of results
total_messages = len(results)
total_errors = len(errors)
total_correct = total_messages - total_errors

print(f"Total messages: {total_messages}")
print(f"Number of errors: {total_errors}")
print(f"Number of correct transmissions: {total_correct}")
print("Test completed and results saved to sensor_can_results.csv and sensor_can_errors.csv")
