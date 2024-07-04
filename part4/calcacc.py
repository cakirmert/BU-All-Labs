import csv
import numpy as np

# Function to read measurements from a CSV file
def read_measurements_from_csv(file_name):
    measurements = []
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header
        for row in reader:
            measurements.append(float(row[0]))  # Ensure the values are floats
    return measurements

# Read measurements from the CSV file
measurements = read_measurements_from_csv('distance_measurements_100cm_500.csv')

# Calculate mean measured duration
mean_measured_duration = np.mean(measurements)

# Calculate the distance in cm
distance = mean_measured_duration / 58.2  # Convert duration to distance

# Actual distance in cm
actual_distance = 100.0

# Calculate absolute error
absolute_error = abs(distance - actual_distance)

# Calculate accuracy
accuracy = (1 - (absolute_error / actual_distance)) * 100

# Calculate standard deviation
std_dev = np.std(measurements)

# Calculate resolution
speed_of_sound = 34300  # Speed of sound in cm/s
time_resolution = 1  # Time resolution in µs
resolution = (speed_of_sound * time_resolution) / 1000000  # Resolution in cm

# Output the results
print(f"Mean Measured Duration: {mean_measured_duration:.2f} µs")
print(f"Calculated Distance: {distance:.2f} cm")
print(f"Actual Distance: {actual_distance:.2f} cm")
print(f"Absolute Error: {absolute_error:.2f} cm")
print(f"Accuracy: {accuracy:.2f} %")
print(f"Standard Deviation: {std_dev:.2f} µs")
print(f"Resolution: {resolution:.4f} cm")
