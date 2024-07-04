import serial  # Import the serial module for communication with the Arduino
import csv  # Import the csv module for writing data to a CSV file
import numpy as np  # Import the numpy module for data manipulation
import matplotlib.pyplot as plt  # Import the matplotlib module for plotting

# Replace 'COM3' with the actual serial port connected to the Arduino
ser = serial.Serial('COM4', 9600)  # Initialize the serial connection
ser.flushInput()  # Clear the input buffer of the serial connection

measurements = []  # Create an empty list to store the measurements
distances = [10, 20, 50, 70, 100]  # Distances in cm to measure

# Collect data for each distance
for distance in distances:
    input(f"Place the sensor at {distance} cm and press Enter")  # Prompt the user to place the sensor at the specified distance
    ser_bytes = ser.readline()  # Read a line of data from the serial connection
    decoded_bytes = int(ser_bytes[0:len(ser_bytes)-1].decode("utf-8"))  # Decode the bytes and convert them to an integer
    print(f"Measured Duration for {distance} cm: {decoded_bytes} µs")  # Print the measured duration
    measurements.append((distance, decoded_bytes))  # Add the distance and measured duration to the measurements list

# Save measurements to CSV
with open("distance_measurements.csv", "w", newline='') as f:  # Open a CSV file for writing
    writer = csv.writer(f)  # Create a CSV writer object
    writer.writerow(["Distance (cm)", "Measured Duration (µs)"])  # Write the header row
    writer.writerows(measurements)  # Write the measurements to the CSV file

# Plot the results
distances, durations = zip(*measurements)  # Unzip the measurements into separate lists
plt.plot(distances, durations, 'bo-')  # Plot the distances vs. durations as blue dots connected by lines
plt.xlabel('Distance (cm)')  # Set the x-axis label
plt.ylabel('Measured Duration (µs)')  # Set the y-axis label
plt.title('Distance vs. Measured Duration')  # Set the plot title
plt.grid(True)  # Enable grid lines
plt.show()  # Display the plot
