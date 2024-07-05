import serial
import time
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# Initialize serial communication with timeout
ser = serial.Serial('COM4', 115200, timeout=2)
time.sleep(2)  # Wait for the connection to be established

def set_dlpf_mode(mode):
    ser.write(str(mode).encode())
    time.sleep(0.1)  # Short delay to ensure command is processed
    # Read the response from Arduino
    response = ser.readline().decode().strip()
    print(f"Response to setting mode {mode}: {response}")

def read_sensor_data_batch(num_samples):
    ser.write(b'M')  # Request a batch of sensor data
    daten = []
    for _ in range(num_samples):
        ser_bytes = ser.readline()
        if ser_bytes:
            try:
                decoded_line = ser_bytes.strip().decode("utf-8")
                print(f"Received: {decoded_line}")
                data = decoded_line.split(",")
                if len(data) == 3:
                    decoded_bytes = int(data[2])  # Get the Z-axis accelerometer data
                    daten.append(decoded_bytes)
            except (UnicodeDecodeError, ValueError) as e:
                print(f"Skipping invalid byte sequence: {e}")
                continue
        else:
            print("No data received from serial port")
            break  # Exit the loop if no data is received to avoid hanging
    return daten

# Define DLPF modes and corresponding names
dlpf_modes = {
    '0': '256Hz',
    '1': '188Hz',
    '2': '98Hz',
    '3': '42Hz',
    '4': '20Hz',
    '5': '10Hz',
    '6': '5Hz'
}

num_samples = 10000  # Number of data points to collect for each mode
all_data = {}

# Loop through each DLPF mode, set it, and collect data
for mode, name in dlpf_modes.items():
    set_dlpf_mode(mode)
    daten = read_sensor_data_batch(num_samples)
    all_data[name] = daten

    # Save data to CSV for each mode
    with open(f"test_data_{name}.csv", "w", newline='') as f:
        writer = csv.writer(f, delimiter=" ")
        for value in daten:
            writer.writerow([value])

    print(f"Data collected for DLPF mode {name}")

# Plotting
plt.figure(figsize=(10, 8))

# Plot time series data for each mode
for name, daten in all_data.items():
    x = np.arange(0, len(daten), 1)
    plt.plot(x, daten, label=f'ACC_Z - {name}')

plt.xlabel('Measurement Number')
plt.ylabel('ACC_Z')
plt.legend()
plt.title('ACC_Z Time Series for Different DLPF Modes')
plt.show()

# Plot histograms for each mode
plt.figure(figsize=(10, 8))
for name, daten in all_data.items():
    plt.hist(daten, bins=100, alpha=0.5, label=f'{name}', range=(min(daten), max(daten)))

plt.xlabel('Value')
plt.ylabel('Frequency')
plt.legend()
plt.title('Histogram for Different DLPF Modes')
plt.show()

# Plot KDE for each mode
plt.figure(figsize=(10, 8))
for name, daten in all_data.items():
    daten = np.array(daten)
    kde = gaussian_kde(daten)
    x_range = np.linspace(min(daten), max(daten), 1000)
    kde_values = kde(x_range)
    plt.plot(x_range, kde_values, label=f'{name}')

plt.xlabel('Value')
plt.ylabel('Density')
plt.legend()
plt.title('Kernel Density Estimation for Different DLPF Modes')
plt.show()

ser.close()
