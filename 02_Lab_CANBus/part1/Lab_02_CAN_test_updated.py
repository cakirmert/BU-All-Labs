import canalystii
import csv
from datetime import datetime
import time  # Import the time module for delays

# Function to send and receive messages
def test_can_settings(bitrate, can_id, remote, extended, data_len, data):
    # Connect to the Canalyst-II device with specified bitrate
    dev = canalystii.CanalystDevice(bitrate=bitrate)
    
    # Receive all pending messages on channel 1 / clear buffer
    for msg in dev.receive(1):
        print(msg)
    
    # Create a new CAN message with the given parameters
    new_message = canalystii.Message(
        can_id=can_id,
        remote=remote,
        extended=extended,
        data_len=data_len,
        data=data
    )
    
    # Send the message on channel 1
    dev.send(1, new_message)
    print(f"Sent: {new_message}")
    
    # Receive the message on channel 1
    received_message = dev.receive(0)
    print(f"Received: {received_message}")
    
    # Log the results
    results.append({
        "bitrate": bitrate,
        "can_id": can_id,
        "remote": remote,
        "extended": extended,
        "data_len": data_len,
        "data": data,
        "sent_message": str(new_message),
        "received_message": str(received_message),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    input(f"Press Enter for next tx/rx")  

    # Stop both channels
    dev.stop(0)
    dev.stop(1)

    # Delete device to free the interface
    del dev

    # Add a short delay to ensure the device is properly released
    time.sleep(1)

# List to store the results
results = []

# Test different settings
test_settings = [
    (500000, 0x3FE, False, False, 8, (1, 2, 3, 4, 5, 6, 7, 8)),
    (250000, 0x1AA, False, True, 4, (10, 20, 30, 40)),
    (125000, 0x2BB, True, False, 8, (100, 101, 102, 103, 104, 105, 106, 107)),
    (1000000, 0x4CC, False, True, 2, (50, 51)),
    (800000, 0x5DD, True, False, 6, (200, 201, 202, 203, 204, 205))
]

for setting in test_settings:
    test_can_settings(*setting)

# Save the results to a CSV file
with open("can_test_results.csv", "w", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["bitrate", "can_id", "remote", "extended", "data_len", "data", "sent_message", "received_message", "timestamp"])
    writer.writeheader()
    for result in results:
        writer.writerow(result)

print("Test completed and results saved to can_test_results.csv")
