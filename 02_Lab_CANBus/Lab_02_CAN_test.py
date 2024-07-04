# -*- coding: utf-8 -*-

# Created on Thu Mar 30 18:15:07 2023

#@author: Rasmus Rettig
# sample code for bus systems lab
# pip install canalystii

import canalystii

# Connect to the Canalyst-II device
# Passing a bitrate to the constructor causes both channels to be initialized and started.
dev = canalystii.CanalystDevice(bitrate=250000)

# Receive all pending messages on channel 0 / clear buffer
for msg in dev.receive(1):
     print(msg)

# sample code for continuous listening:
#while True:
#    msg=dev.receive(0)
#    if msg: print(msg)

# The canalystii.Message class is a ctypes Structure, to minimize overhead

for value in range(2):
   pl=(value, value, value, value, value, value, value, value)
   new_message = canalystii.Message(can_id=0x0AA,
                                 remote=False,
                                 extended=False,
                                 data_len=8,
                                 data=pl)
     # Send one copy to channel 1
   dev.send(1, new_message)

for msg in dev.receive(0):
     print(msg)

# Stop both channels (need to call start() again to resume capturing or send any messages)
dev.stop(0)
dev.stop(1)

# delete dev at the end to free the interface
del dev

