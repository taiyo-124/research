import serial
import time

def read_co2():
	# # シリアルポートの設定
	# ser = serial.Serial(
	# 	port='/dev/ttyAMA4',
	# 	baudrate=9600,
	# 	bytesize=serial.EIGHTBITS,
	# 	parity=serial.PARITY_NONE,
	# 	stopbits=serial.STOPBITS_ONE,
	# 	timeout=1
	# )

	# CO₂ 濃度取得コマンド [SlaveAdd, FuncCode, StartAdd(Up), StartAdd(Down), NumRegister(Up), NumRegister(Down)], CRC, CRC]
	get_command = bytearray([0X68, 0x04, 0x00, 0x03, 0x00, 0x01, 0xC8, 0xF3])
	ser.write(get_command)
	time.sleep(0.1)
	response = ser.read(10)
	# print(response)


	high = response[3]
	low = response[4]
	co2 = (high << 8) | low
	return co2

# シリアルポートの設定
ser = serial.Serial(
		port='/dev/ttyAMA4',
		baudrate=9600,
		bytesize=serial.EIGHTBITS,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		timeout=1
	)

# # Measurement Modeをcontinuous modeに設定
# set_mode_command = bytearray([0x68, 0x10, 0x00, 0x0A, 0x00, 0x01, 0x02, 0x00, 0x64, 0xA8])
# ser.write(set_mode_command)
# time.sleep(1)
# response = ser.read(8)
# print(response)

# CO₂ 濃度の読み取り
while True:
	co2 = read_co2()
	print(f"CO₂ 濃度: {co2} ppm")
	time.sleep(16)