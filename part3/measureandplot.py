import serial  # Import the serial library for serial communication
import csv  # Import the CSV library to handle CSV file operations
import numpy as np  # Import NumPy for numerical operations
import matplotlib.pyplot as plt  # Import Matplotlib for plotting
from scipy.stats import linregress  # Import linregress from SciPy for linear regression

# Replace 'COM4' with actual serial port
ser = serial.Serial('COM4', 9600)  # Initialize serial connection with specified port and baud rate
ser.flushInput()  # Clear the input buffer to start fresh

distances = [10, 20, 30, 40, 50]  # List of distances in cm for measurements
num_measurements = 100  # Number of measurements to be taken per distance
all_measurements = []  # List to store all measurements for all distances
mean_durations = []  # List to store mean durations for each distance

# Function to initiate measurement and read data
def measure_distance():
    ser_bytes = ser.readline()  # Read a line of data from the serial port
    decoded_bytes = int(ser_bytes.decode("utf-8").strip())  # Decode the bytes and convert to an integer
    return decoded_bytes

# Loop through each distance to perform measurements
for distance in distances:
    input(f"Place the sensor at {distance} cm and press Enter to start measurements")  # Prompt user to place sensor at specified distance and start measurement
    measurements = []  # List to store measurements for the current distance
    ser.flushInput()  # Clear the input buffer after user input

    # Collect data for the current distance
    for _ in range(num_measurements):
        decoded_bytes = measure_distance()
        print(f"Measured Duration for {distance} cm: {decoded_bytes} µs")  # Print the measurement to the console
        measurements.append(decoded_bytes)  # Append the measurement to the list

    # Save measurements to a CSV file
    with open(f"distance_measurements_{distance}cm.csv", "w", newline='') as f:
        writer = csv.writer(f)  # Create a CSV writer object
        writer.writerow(["Measured Duration (µs)"])  # Write the header
        writer.writerows([[m] for m in measurements])  # Write the measurements

    # Create and display histogram of the measurements
    plt.hist(measurements, bins='auto')  # Plot histogram with automatic binning
    plt.xlabel('Measured Duration (µs)')  # Label the x-axis
    plt.ylabel('Frequency')  # Label the y-axis
    plt.title(f'Histogram of Measured Durations at {distance} cm')  # Title of the histogram
    plt.savefig(f"histogram_{distance}cm.png")  # Save the histogram as a PNG file
    plt.show()  # Display the histogram

    # Calculate and print the mean value of the measurements
    mean_duration = np.mean(measurements)  # Calculate the mean duration
    print(f"Mean Duration at {distance} cm: {mean_duration} µs")  # Print the mean duration
    mean_durations.append(mean_duration)  # Append the mean duration to the list
    all_measurements.append(measurements)  # Append the measurements to the list of all measurements

# Plot 2T(distance) with a linear trendline
plt.figure()  # Create a new figure
plt.plot(distances, mean_durations, 'bo-', label='Measured Data')  # Plot the measured data
slope, intercept, r_value, p_value, std_err = linregress(distances, mean_durations)  # Perform linear regression
plt.plot(distances, intercept + slope*np.array(distances), 'r--', label='Trendline')  # Plot the trendline
plt.xlabel('Distance (cm)')  # Label the x-axis
plt.ylabel('Mean Measured Duration (µs)')  # Label the y-axis
plt.title('2T vs Distance')  # Title of the plot
plt.legend()  # Display the legend
plt.grid(True)  # Display grid
plt.savefig("2T_vs_Distance.png")  # Save the plot as a PNG file
plt.show()  # Display the plot

# Print the slope and intercept for debugging
print("Slope (µs/cm):", slope)
print("Intercept (µs):", intercept)

# Calculate speed of sound in m/s
# The slope gives us the time for a round trip in µs/cm, so we divide by 2 to get one way in cm
# Then convert to m/s: speed (cm/µs) * 10^4 (µs to s and cm to m)
speed_of_sound = (1 / (slope / 2)) * 1e4
print(f"Calculated speed of sound: {speed_of_sound:.2f} m/s")  # Print the calculated speed of sound

# Identify non-linearity by plotting residuals
residuals = np.array(mean_durations) - (intercept + slope*np.array(distances))  # Calculate residuals
plt.figure()  # Create a new figure
plt.plot(distances, residuals, 'bo-', label='Residuals')  # Plot the residuals
plt.xlabel('Distance (cm)')  # Label the x-axis
plt.ylabel('Residual (µs)')  # Label the y-axis
plt.title('Non-Linearity in Measurements')  # Title of the plot
plt.legend()  # Display the legend
plt.grid(True)  # Display grid
plt.savefig("Non_Linearity.png")  # Save the plot as a PNG file
plt.show()  # Display the plot

# Close the serial connection
ser.close()  # Close the serial port connection
