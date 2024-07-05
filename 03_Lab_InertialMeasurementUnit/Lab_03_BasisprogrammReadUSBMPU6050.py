# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 19:05:31 2020

@author: rrett
"""

import serial
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

ser = serial.Serial('COM4', 9600)
ser.flushInput()
num_samples = 10000  # Number of data points to collect
daten = []

for n in range(0, num_samples):
    ser_bytes = ser.readline()
    try:
        decoded_line = ser_bytes.strip().decode("utf-8")
        data = decoded_line.split(",")
        if len(data) == 6:  # Ensure we have all 6 values (ax, ay, az, gx, gy, gz)
            decoded_bytes = int(data[2])  # Get the Z-axis accelerometer data
            print(decoded_bytes)
            daten.append(decoded_bytes)
            with open("test_data_neu.csv", "a", newline='') as f:
                writer = csv.writer(f, delimiter=" ")
                writer.writerow([decoded_bytes])
    except (UnicodeDecodeError, ValueError) as e:
        print(f"Skipping invalid byte sequence: {e}")
        continue

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
