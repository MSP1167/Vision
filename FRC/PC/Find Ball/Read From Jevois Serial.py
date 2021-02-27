port = 'COM4'

import serial
import time
i = 0

with serial.Serial(port, 115200, timeout=1) as ser:
	while 1:
		# Read a whole line and strip any trailing line ending character
		line = ser.readline().rstrip()
		print (format(line))
		print ("\n {}".format(i))
		i += 1