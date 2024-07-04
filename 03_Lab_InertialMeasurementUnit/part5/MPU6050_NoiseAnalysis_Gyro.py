import serial
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Connect to the Arduino via serial port
arduino_serial = serial.Serial('COM4', 9600)  # Replace 'COM4' with your Arduino's port

def set_bandwidth(bandwidth_command):
    arduino_serial.write(bandwidth_command.encode())
    response = arduino_serial.readline().decode().strip()
    print(response)

def measure_gyro():
    arduino_serial.write('M'.encode())
    gz = int(arduino_serial.readline().decode().strip())
    return gz

def collect_measurements(bandwidth_command, bandwidth_label, output_file, num_samples=1000):
    set_bandwidth(bandwidth_command)
    measurements = []
    for _ in range(num_samples):
        gz = measure_gyro()
        measurements.append(gz)

    with open(output_file, 'a', newline='') as csvfile:
        fieldnames = ['bandwidth', 'measurement']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for m in measurements:
            writer.writerow({'bandwidth': bandwidth_label, 'measurement': m})
    
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
    num_samples = 1000
    output_file = "gyro_noise_analysis.csv"
    
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
        measurements = collect_measurements(bandwidth_command, bandwidth_label, output_file, num_samples)
        mean, std_dev = analyze_measurements(measurements, f"Noise Analysis at {bandwidth_label} (Unfiltered)")
        filtered_measurements = filter_outliers(measurements)
        filtered_mean, filtered_std_dev = analyze_measurements(filtered_measurements, f"Noise Analysis at {bandwidth_label} (Filtered)")
        results.append((bandwidth_label, mean, std_dev, filtered_mean, filtered_std_dev))
    
    print("Bandwidth, Mean (Unfiltered), Std Dev (Unfiltered), Mean (Filtered), Std Dev (Filtered)")
    for result in results:
        print(f"{result[0]}, {result[1]:.2f}, {result[2]:.2f}, {result[3]:.2f}, {result[4]:.2f}")

if __name__ == "__main__":
    main()
