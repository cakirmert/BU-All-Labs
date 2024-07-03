# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 19:05:31 2020

@author: rrett
"""

# Basic program Spyder/Python for course IE6-BUL
# Prof. Dr. Rasmus Rettig

import serial
import csv
import numpy as np
import matplotlib.pyplot as plt
# import time

ser = serial.Serial('/dev/tty.usbserial-14410', 9600)
# the correct serial port and baudrate must be setup (-> arduino software)
# the device must be used in parallel by any other software ('device busy error')
ser.flushInput()
max = 100
data=[]
x = np.arange(0, max, 1) 

for n in range(0, max):
    ser_bytes = ser.readline()
    decoded_bytes = int(ser_bytes[0:len(ser_bytes)-1].decode("utf-8"))
    print(decoded_bytes)
    data.append(decoded_bytes)
    with open("test_data.csv","a", newline='') as f:
        writer = csv.writer(f,delimiter=" ")
        writer.writerow([decoded_bytes])
         # Timestamp: writer.writerow([time.time(),decoded_bytes])

plt.figure(0)
plt.plot(x,data)
plt.xlabel('Measurement Number')
plt.ylabel('Total time of flight in ms')
    
plt.figure(1)        
a=np.hstack(data)
plt.hist(a, bins='auto')
plt.ylabel('Number of measurements')
plt.xlabel('Total time of flight in ms')
plt.show()

print("Mean: ")
print(np.mean(data))

ser.close()