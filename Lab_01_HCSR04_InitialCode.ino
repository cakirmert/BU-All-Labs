
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

void setup()
{
  pinMode(trigger, OUTPUT);
  pinMode(echo, INPUT);
  digitalWrite(trigger, HIGH);
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  // set the data rate for the SoftwareSerial port
  ardunano.begin(9600);
}


void loop() // main loop
{
 int tof = getToF();	// read time of flight
 Serial.print(tof, DEC) ;
 Serial.write("\n"); 
 delay(1000); // wait 1 second
}


/* get time of flight in microseconds
 */
int getToF(){ 
 long time=0;
 digitalWrite(trigger, LOW); 
 delayMicroseconds(3);
 noInterrupts();
 digitalWrite(trigger, HIGH); // trigger impulse 20 us
 delayMicroseconds(20);
 digitalWrite(trigger, LOW); 
 
 
 time = pulseIn(echo, HIGH); // measure echo-time
 interrupts(); 
 return(time); 
}
