# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 19:05:31 2020

@author: rrett
"""

# Basic program Spyder/Python for course IE6-BUL
# Prof. Dr. Rasmus Rettig
# Fit to MPU6050 - Acceleration X-Axis

import serial
import csv
import numpy as np
import matplotlib.pyplot as plt
# import time
# only neccessary, if you want a timestamp

ser = serial.Serial('COM4', 9600)
ser.flushInput()
max = 1000
dataaccx=[]
dataaccy=[]
dataaccz=[]
datagyrx=[]
datagyry=[]
datagyrz=[]
t = np.arange(0, max, 1)

# synchronize to data from arudino (check order!)
while True:
 ser_bytes = ser.readline()
 print(ser_bytes)
 if ser_bytes==b'*\n':
     print('synced')
     break

# start getting data      
for n in range(0, max):
        # 1. Quantity
        ser_bytes = ser.readline()
        decoded_bytes = int(ser_bytes[0:len(ser_bytes)-1].decode("utf-8"))
        print(decoded_bytes)
        dataaccx.append(decoded_bytes)
        # 2. Quantity
        ser_bytes = ser.readline()
        decoded_bytes = int(ser_bytes[0:len(ser_bytes)-1].decode("utf-8"))
        print(decoded_bytes)
        dataaccy.append(decoded_bytes)
        #
        ser_bytes = ser.readline()
        decoded_bytes = int(ser_bytes[0:len(ser_bytes)-1].decode("utf-8"))
        print(decoded_bytes)
        dataaccz.append(decoded_bytes)
        #
        ser_bytes = ser.readline()         
        decoded_bytes = int(ser_bytes[0:len(ser_bytes)-1].decode("utf-8"))
        print(decoded_bytes)
        datagyrx.append(decoded_bytes)        
        #
        ser_bytes = ser.readline()
        decoded_bytes = int(ser_bytes[0:len(ser_bytes)-1].decode("utf-8"))
        print(decoded_bytes)
        datagyry.append(decoded_bytes)        
        #
        ser_bytes = ser.readline()
        decoded_bytes = int(ser_bytes[0:len(ser_bytes)-1].decode("utf-8"))
        print(decoded_bytes)
        datagyrz.append(decoded_bytes)        
        # read sync marker
        ser_bytes = ser.readline()       
     
         
         #with open("test_data_neu.csv","a", newline='') as f:
          #writer = csv.writer(f,delimiter=",")
          #writer.writerow([decoded_bytes])
          # Timestamp: writer.writerow([time.time(),decoded_bytes])   


ser.close()

# plotting

plt.figure(0)
plt.plot(t,dataaccx)
plt.xlabel('Measurement Number')
plt.ylabel('ACC_X')
    
plt.figure(1)        
a=np.hstack(dataaccx)
plt.hist(a, bins='auto')
plt.show()

print("Mean: ")
print(np.mean(dataaccx))

