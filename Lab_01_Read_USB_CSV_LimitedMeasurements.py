# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 19:05:31 2020

@author: rrett
"""

# Basic program Spyder/Python for course IE6-BUL
# Prof. Dr. Rasmus Rettig

import serial  # Import the serial library for serial communication
import csv  # Import the CSV library to handle CSV file operations
import numpy as np  # Import NumPy for numerical operations
import matplotlib.pyplot as plt  # Import Matplotlib for plotting

# Replace 'COM3' with specific serial port
# check Device Manager for the exact port
ser = serial.Serial('COM3', 9600)  # Initialize serial connection with specified port and baud rate
ser.flushInput()  # Clear the input buffer to start fresh

max = 100  # Number of measurements to be taken
data = []  # List to store the measurement data
x = np.arange(0, max, 1)  # Create an array of numbers from 0 to max-1 for x-axis values

# Loop to read and store measurements
for n in range(0, max):
    ser_bytes = ser.readline()  # Read a line of data from the serial port
    decoded_bytes = int(ser_bytes[0:len(ser_bytes)-1].decode("utf-8"))  # Decode the bytes and convert to an integer
    print(decoded_bytes)  # Print the measurement to the console
    data.append(decoded_bytes)  # Append the measurement to the data list
    with open("test_data.csv", "a", newline='') as f:  # Open the CSV file in append mode
        writer = csv.writer(f, delimiter=" ")  # Create a CSV writer object
        writer.writerow([decoded_bytes])  # Write the measurement to the CSV file

# Plot the measurements over the number of measurements
plt.figure(0)  # Create a new figure
plt.plot(x, data)  # Plot data against x-axis values
plt.xlabel('Measurement Number')  # Label the x-axis
plt.ylabel('Total time of flight in ms')  # Label the y-axis

# Plot a histogram of the measurements
plt.figure(1)  # Create a new figure
a = np.hstack(data)  # Convert the list to a NumPy array
plt.hist(a, bins='auto')  # Plot a histogram with automatic binning
plt.ylabel('Number of measurements')  # Label the y-axis
plt.xlabel('Total time of flight in ms')  # Label the x-axis
plt.show()  # Display the plots

# Calculate and print the mean of the measurements
print("Mean: ")  # Print "Mean: " to the console
print(np.mean(data))  # Calculate and print the mean of the data

# Close the serial connection
ser.close()  # Close the serial port connection
