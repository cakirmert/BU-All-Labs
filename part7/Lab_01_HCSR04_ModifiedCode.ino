#include <SoftwareSerial.h>

#define trigger 3  // Arduino Pin to HC-SR04 Trig
#define echo 2     // Arduino Pin to HC-SR04 Echo
#define ledPin 13  // Arduino Pin for LED

SoftwareSerial ardunano(11, 12);

void setup() {
  pinMode(trigger, OUTPUT);    // Set the trigger pin as an output
  pinMode(echo, INPUT);        // Set the echo pin as an input
  pinMode(ledPin, OUTPUT);     // Set the LED pin as an output
  digitalWrite(trigger, LOW);  // Ensure trigger pin is LOW initially
  Serial.begin(9600);          // Start the hardware serial communication at 9600 baud rate
  ardunano.begin(9600);        // Start the software serial communication at 9600 baud rate
}

void loop() {
  long duration = getToF();  // Read time of flight
  float distance = duration * 0.034 / 2;  // Calculate distance in cm (speed of sound = 0.034 cm/µs)
  Serial.print(distance);  // Print the distance in cm
  Serial.write(" cm\n");  // Send a newline character

  if (distance < 200) {
    digitalWrite(ledPin, HIGH);  // Turn on the LED if the object is closer than 2 meters
  } else if (distance > 210) {
    digitalWrite(ledPin, LOW);  // Turn off the LED if the object is farther than 2.10 meters
  }

  delay(1000);  // Wait for 1 second
}

/* Function to get time of flight in microseconds */
long getToF() { 
  long time = 0;
  digitalWrite(trigger, LOW); 
  delayMicroseconds(2);
  digitalWrite(trigger, HIGH);  // Trigger impulse for 10 microseconds
  delayMicroseconds(10);
  digitalWrite(trigger, LOW); 
  time = pulseIn(echo, HIGH);  // Measure echo time
  return time;  // Return the measured time
}
