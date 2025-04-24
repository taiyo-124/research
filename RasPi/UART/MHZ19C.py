import serial
import time 


def read_co2():
	ser = serial.Serial(
		port='/dev/ttyAMA4',
		baudrate=9600,
		bytesize=serial.EIGHTBITS,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		timeout=1
	)
	
	request = bytearray([0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])
	ser.write(request)
	time.sleep(0.1)
	response = ser.read(9)
	ser.close()
	
	print(response)
	
	# if len(response) == 9 and response[0] == 0xFF and response[1] == 0x86:
	if len(response) == 9:
		high = response[2]
		low = response[3]
		co2 = (high << 8) | low
		return co2
	else:
		return None
		
try:
	while True:
		co2 = read_co2()
		if co2 is not None:
			print(f"CO2: {co2}ppm")
		else:
			print("No data")
		time.sleep(1)
except KeyboardInterrupt:
	print("finish")

finally:
	ser.close()
	print("serial port closed")
