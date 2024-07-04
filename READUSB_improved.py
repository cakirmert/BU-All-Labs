# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 19:05:31 2020

@author: rrett
"""

# Basic program Spyder/Python for course IE6-BUL
# Prof. Dr. Rasmus Rettig
# Modified by: Mert Cakir to include actual distance input and multiple segments

import serial  # Import the serial library for serial communication
import csv  # Import the CSV library to handle CSV file operations
import numpy as np  # Import NumPy for numerical operations
import matplotlib.pyplot as plt  # Import Matplotlib for plotting

# Replace 'COM3' with specific serial port
# check Device Manager for the exact port
ser = serial.Serial('COM4', 9600)  # Initialize serial connection with specified port and baud rate
ser.flushInput()  # Clear the input buffer to start fresh

total_measurements = 100  # Total number of measurements to be taken
num_segments = 4  # Number of segments to divide the measurements into
measurements_per_segment = total_measurements // num_segments  # Measurements per segment
data = []  # List to store the measurement data
actual_distances = []  # List to store the actual distances

with open("distance_data.csv", "w", newline='') as f:  # Open the CSV file in write mode
    writer = csv.writer(f)
    writer.writerow(["Actual Distance (cm)", "Measured Distance (cm)"])  # Write headers

    for segment in range(num_segments):
        # Prompt to enter the actual distance for this segment
        actual_distance = float(input(f"Enter the actual distance for segment {segment + 1}: "))
        actual_distances.extend([actual_distance] * measurements_per_segment)

        # Take measurements for the given actual distance
        for _ in range(measurements_per_segment):
            ser_bytes = ser.readline()  # Read a line of data from the serial port
            decoded_bytes = int(ser_bytes[0:len(ser_bytes)-1].decode("utf-8"))  # Decode the bytes and convert to an integer
            print(f"Actual: {actual_distance}, Measured: {decoded_bytes}")  # Print the actual and measured distances
            data.append(decoded_bytes)  # Append the measured distance to the data list
            writer.writerow([actual_distance, decoded_bytes])  # Write the actual and measured distances to the CSV file

# Plot the measurements over the number of measurements
x = np.arange(0, total_measurements, 1)  # Create an array of numbers from 0 to total_measurements-1 for x-axis values
plt.figure(0)  # Create a new figure
plt.plot(x, data)  # Plot data against x-axis values
plt.xlabel('Measurement Number')  # Label the x-axis
plt.ylabel('Measured Distance (cm)')  # Label the y-axis

# Plot a histogram of the measurements
plt.figure(1)  # Create a new figure
a = np.hstack(data)  # Convert the list to a NumPy array
plt.hist(a, bins='auto')  # Plot a histogram with automatic binning
plt.ylabel('Number of measurements')  # Label the y-axis
plt.xlabel('Measured Distance (cm)')  # Label the x-axis
plt.show()  # Display the plots

# Calculate and print the mean of the measurements
print("Mean: ")  # Print "Mean: " to the console
print(np.mean(data))  # Calculate and print the mean of the data

# Close the serial connection
ser.close()  # Close the serial port connection
