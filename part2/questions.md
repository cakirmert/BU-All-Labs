# Which line in the code is related to which edge/pulse on the screen?

## Answer: The line digitalWrite(trigger, HIGH); in the Arduino code corresponds to the rising edge of the trigger pulse. The line time = pulseIn(echo, HIGH); corresponds to the duration of the echo pulse.

# How are the signals related?

## Answer: The trigger signal initiates the ultrasonic pulse, and the echo signal represents the time it takes for the pulse to travel to the object and back. The duration of the echo pulse is directly related to the distance of the object.

# What is the measurement frequency?

## Answer: The measurement frequency is determined by the loop delay in the Arduino code, which is set to 1 second (delay(1000);). This means the sensor takes a measurement every second.