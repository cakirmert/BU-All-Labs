# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 19:05:31 2020

@author: rrett
"""

# Basisprogramm Spyder/Python zum Kurs Sensorik im Sommersemester 2020
# Prof. Dr. Rasmus Rettig
# Anpassung für MPU6050 - Beschleunigung X-Kanal

import serial
import csv
import numpy as np
import matplotlib.pyplot as plt
# import time
# nur erforderlich, wenn ein Zeitstempel erzeugt werden soll

ser = serial.Serial('COM4', 9600)
ser.flushInput()
max = 10
daten=[]
x = np.arange(0, max, 1)

for n in range(0, max):
    ser_bytes = ser.readline()
    decoded_bytes = int(ser_bytes[0:len(ser_bytes)-1].decode("utf-8"))
    print(decoded_bytes)
    daten.append(decoded_bytes)
    with open("test_data_neu.csv","a", newline='') as f:
        writer = csv.writer(f,delimiter=" ")
        writer.writerow([decoded_bytes])
         # Zeitstempel: writer.writerow([time.time(),decoded_bytes])

plt.figure(0)
plt.plot(x,daten)
plt.xlabel('Measurement Number')
plt.ylabel('ACC_X')
    
plt.figure(1)        
a=np.hstack(daten)
plt.hist(a, bins='auto')
plt.show()

print("Mittelwert: ")
print(np.mean(daten))

ser.close()