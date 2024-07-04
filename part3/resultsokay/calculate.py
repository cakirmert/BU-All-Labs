import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# List of distances in cm for measurements
distances = [10, 20, 30, 40, 50]
mean_durations = []  # List to store mean durations for each distance

# Function to read measurements from a CSV file
def read_measurements_from_csv(file_name):
    measurements = []
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header
        for row in reader:
            measurements.append(int(row[0]))
    return measurements

# Read measurements and calculate mean durations
for distance in distances:
    file_name = f"distance_measurements_{distance}cm.csv"
    measurements = read_measurements_from_csv(file_name)
    mean_duration = np.mean(measurements)
    mean_durations.append(mean_duration)

# Print mean durations for debugging
print("Distances (cm):", distances)
print("Mean Durations (µs):", mean_durations)

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
