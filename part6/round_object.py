import serial
import csv

# Replace 'COM3' with actual serial port
ser = serial.Serial('COM3', 9600)
ser.flushInput()

num_measurements = 10  # Number of measurements per position
positions = ["center", "left", "right"]
results = {}
expected_distance = 50  # Expected distance in cm
threshold = 5  # Threshold for correct measurement in cm

for position in positions:
    input(f"Place the round object in the {position} position and press Enter")
    measurements = []

    # Collect data
    for _ in range(num_measurements):
        ser_bytes = ser.readline()
        decoded_bytes = float(ser_bytes.decode("utf-8").strip(" cm\n"))
        print(f"Measured Distance in {position} position: {decoded_bytes} cm")
        measurements.append(decoded_bytes)

    mean_distance = sum(measurements) / len(measurements)
    correct_measurement = "yes" if abs(mean_distance - expected_distance) < threshold else "no"
    results[position] = (mean_distance, correct_measurement)

# Close the serial connection
ser.close()

# Save results to CSV
with open("round_object_results.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Position", "Mean Distance (cm)", "Correct Measurement"])
    for position, (mean_distance, correct_measurement) in results.items():
        writer.writerow([position, mean_distance, correct_measurement])

# Print results
for position, (mean_distance, correct_measurement) in results.items():
    print(f"Position: {position}, Mean Distance: {mean_distance} cm, Correct: {correct_measurement}")
