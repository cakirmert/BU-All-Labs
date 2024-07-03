
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
  digitalWrite(trigger, HIGH); // Set the trigger pin to HIGH (unusual for HC-SR04 setup)
  Serial.begin(9600); // Start the hardware serial communication at 9600 baud rate
  ardunano.begin(9600); // Start the software serial communication at 9600 baud rate
}

void loop() {
  int tof = getToF(); // Read time of flight
  Serial.print(tof, DEC); // Print the time of flight in decimal format
  Serial.write("\n"); // Send a newline character
  delay(1000); // Wait for 1 second
}

/* Function to get time of flight in microseconds */
int getToF() { 
  long time = 0;
  digitalWrite(trigger, LOW); 
  delayMicroseconds(3);
  noInterrupts(); // Disable interrupts for precise timing
  digitalWrite(trigger, HIGH); // Trigger impulse for 20 microseconds
  delayMicroseconds(20);
  digitalWrite(trigger, LOW); 
  time = pulseIn(echo, HIGH); // Measure echo time
  interrupts(); // Enable interrupts
  return time; // Return the measured time
}
