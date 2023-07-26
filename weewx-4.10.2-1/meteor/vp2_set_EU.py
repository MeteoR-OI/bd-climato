#/bin/python

import serial


PORT = '/dev/vp2' 


ser = serial.Serial(PORT, 19200, timeout=2)

ser.write("TST 1\n")
buf = ser.read(99)
print buf

ser.write("BAND 1\n")
buf = ser.read(99)
print buf

ser.write("DOMAIN 2\n")
buf = ser.read(99)
print buf

ser.write("TST 0\n")
buf = ser.read(99)
print buf

ser.close()


