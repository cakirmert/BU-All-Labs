import serial
import time
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import gaussian_kde

# Connect to the Arduino via serial port
arduino_serial = serial.Serial('COM4', 115200, timeout=2)  # Replace 'COM4' with your Arduino's port
time.sleep(2)  # Wait for the connection to be established

def set_bandwidth(bandwidth_command):
    arduino_serial.write(bandwidth_command.encode())
    response = arduino_serial.readline().decode().strip()
    print(response)

def measure_gyro_batch(num_samples):
    arduino_serial.write(b'M')
    measurements = []
    for _ in range(num_samples):
        gz = arduino_serial.readline().decode().strip()
        if gz:
            try:
                measurements.append(int(gz))
            except ValueError:
                print(f"Skipping invalid value: {gz}")
    return measurements

def collect_measurements(bandwidth_command, bandwidth_label, num_samples=1000):
    set_bandwidth(bandwidth_command)
    measurements = measure_gyro_batch(num_samples)
    return measurements

def filter_outliers(data, threshold=3):
    mean = np.mean(data)
    std_dev = np.std(data)
    filtered_data = [x for x in data if (mean - threshold * std_dev < x < mean + threshold * std_dev)]
    return filtered_data

def analyze_measurements(measurements, title):
    mean_value = np.mean(measurements)
    std_deviation = np.std(measurements)
    
    plt.hist(measurements, bins=30, density=True, alpha=0.6, color='g')
    
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mean_value, std_deviation)
    plt.plot(x, p, 'k', linewidth=2)
    
    title = f"{title}\nMean = {mean_value:.2f}, Std Dev = {std_deviation:.2f}"
    plt.title(title)
    plt.xlabel('Angular Rate (gz)')
    plt.ylabel('Density')
    
    plt.show()
    return mean_value, std_deviation

def main():
    num_samples = 10000
    bandwidths = [
        ('0', "256Hz"),
        ('1', "188Hz"),
        ('2', "98Hz"),
        ('3', "42Hz"),
        ('4', "20Hz"),
        ('5', "10Hz"),
        ('6', "5Hz")
    ]
    
    all_data = {}
    results = []
    
    # Collect measurements for each bandwidth
    for bandwidth_command, bandwidth_label in bandwidths:
        measurements = collect_measurements(bandwidth_command, bandwidth_label, num_samples)
        all_data[bandwidth_label] = measurements
        mean, std_dev = analyze_measurements(measurements, f"Noise Analysis at {bandwidth_label} (Unfiltered)")
        filtered_measurements = filter_outliers(measurements)
        filtered_mean, filtered_std_dev = analyze_measurements(filtered_measurements, f"Noise Analysis at {bandwidth_label} (Filtered)")
        results.append((bandwidth_label, mean, std_dev, filtered_mean, filtered_std_dev))
    
    print("Bandwidth, Mean (Unfiltered), Std Dev (Unfiltered), Mean (Filtered), Std Dev (Filtered)")
    for result in results:
        print(f"{result[0]}, {result[1]:.2f}, {result[2]:.2f}, {result[3]:.2f}, {result[4]:.2f}")

    # Plot all data together
    plt.figure(figsize=(10, 8))

    # Plot time series data for each mode
    for name, measurements in all_data.items():
        x = np.arange(0, len(measurements), 1)
        plt.plot(x, measurements, label=f'Gyro_Z - {name}')

    plt.xlabel('Measurement Number')
    plt.ylabel('Gyro_Z')
    plt.legend()
    plt.title('Gyro_Z Time Series for Different DLPF Modes')
    plt.show()

    # Plot histograms for each mode
    plt.figure(figsize=(10, 8))
    for name, measurements in all_data.items():
        plt.hist(measurements, bins=100, alpha=0.5, label=f'{name}', range=(min(measurements), max(measurements)))

    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.legend()
    plt.title('Histogram for Different DLPF Modes')
    plt.show()

    # Plot KDE for each mode
    plt.figure(figsize=(10, 8))
    for name, measurements in all_data.items():
        measurements = np.array(measurements)
        kde = gaussian_kde(measurements)
        x_range = np.linspace(min(measurements), max(measurements), 1000)
        kde_values = kde(x_range)
        plt.plot(x_range, kde_values, label=f'{name}')

    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.legend()
    plt.title('Kernel Density Estimation for Different DLPF Modes')
    plt.show()

if __name__ == "__main__":
    main()
