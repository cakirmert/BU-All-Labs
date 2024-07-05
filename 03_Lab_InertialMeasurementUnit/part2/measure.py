import serial
import time
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# Initialize serial communication
ser = serial.Serial('COM4', 115200)
time.sleep(2)  # Wait for the connection to be established

def set_accel_range(range_code):
    ser.write(range_code.encode())
    time.sleep(0.1)  # Short delay to ensure command is processed

def read_sensor_data(num_samples):
    daten = []
    for _ in range(num_samples):
        ser.write(b'M')  # Request sensor data
        ser_bytes = ser.readline()
        try:
            decoded_line = ser_bytes.strip().decode("utf-8")
            data = decoded_line.split(",")
            if len(data) == 6:
                decoded_bytes = int(data[2])  # Get the Z-axis accelerometer data
                daten.append(decoded_bytes)
        except (UnicodeDecodeError, ValueError) as e:
            print(f"Skipping invalid byte sequence: {e}")
            continue
    return daten

# Set accelerometer range (0 for ±2g, 1 for ±4g, 2 for ±8g, 3 for ±16g)
set_accel_range('0')

# Read sensor data
num_samples = 10000
daten = read_sensor_data(num_samples)

# Save data to CSV
with open("test_data_neu.csv", "w", newline='') as f:
    writer = csv.writer(f, delimiter=" ")
    for value in daten:
        writer.writerow([value])

# Create x based on the length of daten
x = np.arange(0, len(daten), 1)

plt.figure(0)
plt.plot(x, daten)
plt.xlabel('Measurement Number')
plt.ylabel('ACC_Z')

# Using increased number of bins and range adjustment
plt.figure(1)
plt.hist(daten, bins=100, range=(min(daten), max(daten)))  # Adjust the number of bins and range
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram with Increased Bins')
plt.show()

# Using Kernel Density Estimation (KDE) for a smoother plot
daten = np.array(daten)
kde = gaussian_kde(daten)
x_range = np.linspace(min(daten), max(daten), 1000)
kde_values = kde(x_range)

plt.figure(2)
plt.plot(x_range, kde_values)
plt.xlabel('Value')
plt.ylabel('Density')
plt.title('Kernel Density Estimation')
plt.show()

print("Mittelwert: ")
print(np.mean(daten))

ser.close()
