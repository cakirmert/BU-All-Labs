import serial
import csv
import numpy as np
import matplotlib.pyplot as plt

# Replace 'COM3' with actual serial port
ser = serial.Serial('COM3', 9600)  # Initialize serial connection with specified port and baud rate
ser.flushInput()  # Clear the input buffer to start fresh

distances = [20, 50, 100, 200]  # Distances in cm
num_measurements = 50  # Number of measurements per distance
all_measurements = []  # To store all measurements for all distances
mean_distances = []  # To store mean distances for each distance

for distance in distances:
    input(f"Place the sensor at {distance} cm and press Enter")  # Prompt user to position the sensor
    measurements = []  # List to store measurements for the current distance

    # Collect data
    for _ in range(num_measurements):
        ser_bytes = ser.readline()  # Read a line of data from the serial port
        decoded_bytes = float(ser_bytes.decode("utf-8").strip(" cm\n"))  # Decode the bytes and convert to float
        print(f"Measured Distance for {distance} cm: {decoded_bytes} cm")  # Print the measurement to the console
        measurements.append(decoded_bytes)  # Append the measurement to the list

    # Save measurements to CSV
    with open(f"distance_measurements_{distance}cm.csv", "w", newline='') as f:
        writer = csv.writer(f)  # Create a CSV writer object
        writer.writerow(["Measured Distance (cm)"])  # Write the header
        writer.writerows([[m] for m in measurements])  # Write the measurements

    # Calculate and print mean value
    mean_distance = np.mean(measurements)  # Calculate the mean distance
    print(f"Mean Distance at {distance} cm: {mean_distance} cm")  # Print the mean distance
    mean_distances.append(mean_distance)  # Append the mean distance to the list
    all_measurements.append(measurements)  # Append the measurements to the list of all measurements

# Close the serial connection
ser.close()  # Close the serial port connection

# Plot the measured distances
plt.figure()
plt.plot(distances, mean_distances, 'bo-', label='Measured Data')
plt.xlabel('Actual Distance (cm)')  # Label the x-axis
plt.ylabel('Mean Measured Distance (cm)')  # Label the y-axis
plt.title('Measured Distance vs Actual Distance')  # Title of the plot
plt.legend()
plt.grid(True)
plt.savefig("Measured_vs_Actual_Distance.png")  # Save the plot as a PNG file
plt.show()

# Calculate and print maximum error
errors = [abs(actual - measured) for actual, measured in zip(distances, mean_distances)]
max_error = max(errors)
print(f"Maximum error: {max_error} cm")
