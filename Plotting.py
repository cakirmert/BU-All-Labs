import csv
import numpy as np
import matplotlib.pyplot as plt

# Initialize lists to hold the actual and measured distances
actual_distances = []
measured_distances = []

# Read data from CSV file
with open('distance_data.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        actual_distances.append(float(row['Actual Distance (cm)']))
        measured_distances.append(float(row['Measured Distance (cm)']))

# Convert lists to NumPy arrays for easier handling
actual_distances = np.array(actual_distances)
measured_distances = np.array(measured_distances)

# Plot the actual distances vs. measured distances
plt.figure(1)
plt.plot(actual_distances, measured_distances, 'bo-', label='Measured Data')
plt.plot(actual_distances, actual_distances, 'r--', label='Ideal Line')
plt.xlabel('Actual Distance (cm)')
plt.ylabel('Measured Distance (cm)')
plt.title('HC-SR04 Sensor Characteristic Curve')
plt.legend()
plt.grid(True)

# Calculate the errors
errors = measured_distances - actual_distances

# Plot the errors
plt.figure(2)
plt.plot(actual_distances, errors, 'bo-', label='Errors')
plt.axhline(0, color='r', linestyle='--', label='Ideal Line')
plt.xlabel('Actual Distance (cm)')
plt.ylabel('Error (Measured - Actual) (cm)')
plt.title('HC-SR04 Measurement Errors')
plt.legend()
plt.grid(True)

plt.show()
