import serial
import csv
import numpy as np
from scipy.stats import norm

import matplotlib.pyplot as plt

# Connect to the Arduino via serial port
arduino_serial = serial.Serial('COM4', 9600) 

def set_bandwidth(bandwidth_command):
    # Send the bandwidth command to the Arduino
    arduino_serial.write(bandwidth_command.encode())
    # Read the response from the Arduino
    response = arduino_serial.readline().decode().strip()
    print(response)

def measure_accelerometer():
    # Send the measurement command to the Arduino
    arduino_serial.write('M'.encode())
    # Read the accelerometer data from the Arduino
    data = arduino_serial.readline().decode().strip().split(',')
    ax, ay, az = map(int, data)
    return ax

def collect_measurements(bandwidth_command, bandwidth_label, output_file, num_samples=1000):
    # Set the bandwidth on the Arduino
    set_bandwidth(bandwidth_command)
    measurements = []
    for _ in range(num_samples):
        # Measure the accelerometer data
        ax = measure_accelerometer()
        measurements.append(ax)

    # Write the measurements to a CSV file
    with open(output_file, 'a', newline='') as csvfile:
        fieldnames = ['bandwidth', 'measurement']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for m in measurements:
            writer.writerow({'bandwidth': bandwidth_label, 'measurement': m})
    
    return measurements

def analyze_measurements(measurements, title):
    # Calculate the mean and standard deviation of the measurements
    mean_value = np.mean(measurements)
    std_deviation = np.std(measurements)
    
    # Plot a histogram of the measurements
    plt.hist(measurements, bins=30, density=True, alpha=0.6, color='g')
    
    # Plot the normal distribution curve
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mean_value, std_deviation)
    plt.plot(x, p, 'k', linewidth=2)
    
    # Add title and labels to the plot
    title = f"{title}\nMean = {mean_value:.2f}, Std Dev = {std_deviation:.2f}"
    plt.title(title)
    plt.xlabel('Acceleration (ax)')
    plt.ylabel('Density')
    
    # Show the plot
    plt.show()
    return mean_value, std_deviation

def main():
    num_samples = 1000
    output_file = "accelerometer_noise_analysis.csv"
    
    bandwidths = [
        ('0', "256Hz"),
        ('1', "188Hz"),
        ('2', "98Hz"),
        ('3', "42Hz"),
        ('4', "20Hz"),
        ('5', "10Hz"),
        ('6', "5Hz")
    ]
    
    results = []
    for bandwidth_command, bandwidth_label in bandwidths:
        # Collect measurements for each bandwidth
        measurements = collect_measurements(bandwidth_command, bandwidth_label, output_file, num_samples)
        # Analyze the measurements and store the results
        mean, std_dev = analyze_measurements(measurements, f"Noise Analysis at {bandwidth_label}")
        results.append((bandwidth_label, mean, std_dev))
    
    # Print the results
    print("Bandwidth, Mean, Std Dev")
    for result in results:
        print(f"{result[0]}, {result[1]:.2f}, {result[2]:.2f}")

if __name__ == "__main__":
    main()
