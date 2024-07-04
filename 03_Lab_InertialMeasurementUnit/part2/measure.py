import smbus
import time
import csv

# MPU-6050 Registers and their addresses
PWR_MGMT_1 = 0x6B
ACCEL_CONFIG = 0x1C
ACCEL_XOUT_H = 0x3B

# Initialize the MPU-6050
def MPU_Init(bus, device_address):
    bus.write_byte_data(device_address, PWR_MGMT_1, 0)  # Write to power management register to wake up the sensor

# Read raw data from MPU-6050
def read_raw_data(bus, addr, device_address):
    high = bus.read_byte_data(device_address, addr)
    low = bus.read_byte_data(device_address, addr + 1)
    value = ((high << 8) | low)
    if value > 32768:
        value = value - 65536
    return value

# Set accelerometer range
def set_accelerometer_range(bus, device_address, range_setting):
    bus.write_byte_data(device_address, ACCEL_CONFIG, range_setting << 3)

# Collect and log measurements for the given range
def collect_measurements(bus, device_address, accel_range, range_label, output_file):
    set_accelerometer_range(bus, device_address, accel_range)
    with open(output_file, 'a', newline='') as csvfile:
        fieldnames = ['range', 'position', 'accel_x']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        positions = ['-1g', '0g', '+1g']
        print(f"Collecting measurements for range: {range_label}")
        for position in positions:
            input(f"Place the sensor at {position} (e.g., {position} along X-axis) and press Enter to measure.")
            accel_x = read_raw_data(bus, ACCEL_XOUT_H, device_address)
            print(f"Measured accel_x for {position}: {accel_x}")
            writer.writerow({'range': range_label, 'position': position, 'accel_x': accel_x})

def main():
    bus = smbus.SMBus(1)  # Initialize I2C bus
    device_address = 0x68  # MPU-6050 device address

    # Initialize MPU-6050
    MPU_Init(bus, device_address)

    # Output file for measurements
    output_file = input("Enter the output CSV file name: ")

    # Collect measurements for different ranges
    ranges = [
        (0, "±2g"),
        (1, "±4g"),
        (2, "±8g"),
        (3, "±16g")
    ]
    for accel_range, range_label in ranges:
        collect_measurements(bus, device_address, accel_range, range_label, output_file)

    print(f"Measurements collected and saved to {output_file}")

if __name__ == "__main__":
    main()
