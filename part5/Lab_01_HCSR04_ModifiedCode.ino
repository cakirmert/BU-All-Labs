
// Basic programm Ultrasonic sensor HC-SR04
// Prof. Dr. Rasmus Rettig
// HC-SR04 Ultraschallsensor
// Connections: 5V-5V, GND-GND, D2-Echo, D3-Trig
// you may need to install libraries via "tools/manage libraries"
// revision 22.6.24 

#include <SoftwareSerial.h>

#define trigger 3 // Arduino Pin to HC-SR04 Trig
#define echo 2    // Arduino Pin to HC-SR04 Echo

SoftwareSerial ardunano(11, 12);

void setup() {
  pinMode(trigger, OUTPUT); // Set the trigger pin as an output
  pinMode(echo, INPUT); // Set the echo pin as an input
  digitalWrite(trigger, HIGH); // Set the trigger pin to HIGH initially, but it will be LOW when sending the trigger impulse
  Serial.begin(9600); // Start the hardware serial communication at 9600 baud rate
  ardunano.begin(9600); // Start the software serial communication at 9600 baud rate
}

void loop() {
  long duration = getToF(); // Read time of flight
  float distance = duration * 0.034 / 2; // Calculate distance in cm (speed of sound = 0.034 cm/µs)
  Serial.print(distance); // Print the distance in cm
  Serial.write(" cm\n"); // Send a newline character
  delay(1000); // Wait for 1 second
}

/* Function to get time of flight in microseconds */
long getToF() { 
  long time = 0;
  digitalWrite(trigger, LOW); 
  delayMicroseconds(2);
  noInterrupts(); // Disable interrupts for precise timing
  digitalWrite(trigger, HIGH); // Trigger impulse for 10 microseconds
  delayMicroseconds(10);
  digitalWrite(trigger, LOW); 
  time = pulseIn(echo, HIGH); // Measure echo time
  interrupts(); // Enable interrupts
  return time; // Return the measured time
}
