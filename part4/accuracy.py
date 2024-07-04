import serial
import csv
import numpy as np
import matplotlib.pyplot as plt

# Replace 'COM3' with your actual serial port
ser = serial.Serial('COM3', 9600)  # Initialize serial connection with specified port and baud rate
ser.flushInput()  # Clear the input buffer to start fresh

distance = 100  # Distance in cm for the measurement
num_measurements = 500  # Number of measurements to be taken
measurements = []  # List to store the measurement data

input(f"Place the sensor at {distance} cm and press Enter")  # Prompt user to position the sensor

# Collect data
for _ in range(num_measurements):
    ser_bytes = ser.readline()  # Read a line of data from the serial port
    decoded_bytes = int(ser_bytes[0:len(ser_bytes)-1].decode("utf-8"))  # Decode the bytes and convert to an integer
    print(f"Measured Duration for {distance} cm: {decoded_bytes} µs")  # Print the measurement to the console
    measurements.append(decoded_bytes)  # Append the measurement to the list

# Save measurements to CSV
with open(f"distance_measurements_{distance}cm_500.csv", "w", newline='') as f:
    writer = csv.writer(f)  # Create a CSV writer object
    writer.writerow(["Measured Duration (µs)"])  # Write the header
    writer.writerows([[m] for m in measurements])  # Write the measurements

# Plot histograms with different bin sizes
bin_sizes = [10, 20, 50]  # Different bin sizes for the histogram
for bins in bin_sizes:
    plt.hist(measurements, bins=bins)  # Plot histogram with specified bin size
    plt.xlabel('Measured Duration (µs)')  # Label the x-axis
    plt.ylabel('Frequency')  # Label the y-axis
    plt.title(f'Histogram of Measured Durations at {distance} cm with {bins} Bins')  # Title of the histogram
    plt.savefig(f"histogram_{distance}cm_500_{bins}bins.png")  # Save the histogram as a PNG file
    plt.show()  # Display the histogram

# Calculate and print mean and standard deviation
mean_duration = np.mean(measurements)  # Calculate the mean duration
std_dev_duration = np.std(measurements)  # Calculate the standard deviation
print(f"Mean Duration at {distance} cm: {mean_duration} µs")  # Print the mean duration
print(f"Standard Deviation at {distance} cm: {std_dev_duration} µs")  # Print the standard deviation

# Close the serial connection
ser.close()  # Close the serial port connection
