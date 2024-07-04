import serial
import csv

# Connect to the Arduino via serial port
arduino_serial = serial.Serial('COM4', 9600)  # Replace 'COM4' with your Arduino's port

def set_accelerometer_range(range_command):
    arduino_serial.write(range_command.encode())
    response = arduino_serial.readline().decode().strip()
    print(response)

def measure_accelerometer():
    arduino_serial.write('M'.encode())
    data = arduino_serial.readline().decode().strip().split(',')
    ax, ay, az, gx, gy, gz = map(int, data)
    return ax, ay, az, gx, gy, gz

def collect_measurements(range_command, range_label, output_file):
    set_accelerometer_range(range_command)
    with open(output_file, 'a', newline='') as csvfile:
        fieldnames = ['range', 'position', 'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        positions = ['-1g', '0g', '+1g']
        print(f"Collecting measurements for range: {range_label}")
        for position in positions:
            input(f"Place the sensor at {position} (e.g., {position} along X-axis) and press Enter to measure.")
            ax, ay, az, gx, gy, gz = measure_accelerometer()
            print(f"Measured accel_x: {ax}, accel_y: {ay}, accel_z: {az}, gyro_x: {gx}, gyro_y: {gy}, gyro_z: {gz} for {position}")
            writer.writerow({'range': range_label, 'position': position, 'accel_x': ax, 'accel_y': ay, 'accel_z': az, 'gyro_x': gx, 'gyro_y': gy, 'gyro_z': gz})

def main():
    # Output file for measurements
    output_file = input("Enter the output CSV file name: ")

    # Collect measurements for different ranges
    ranges = [
        ('0', "±2g"),
        ('1', "±4g"),
        ('2', "±8g"),
        ('3', "±16g")
    ]
    for range_command, range_label in ranges:
        collect_measurements(range_command, range_label, output_file)

    print(f"Measurements collected and saved to {output_file}")

if __name__ == "__main__":
    main()
