import serial
import time

from datetime import datetime
import os


# CO2濃度をセンシング
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
	# print(len(response))


	high = response[3]
	low = response[4]
	co2 = (high << 8) | low
	return co2


# SDカードに保存(path)
def writeSD(Datafile, Errorfile, data):
	# 時刻情報取得
	now = datetime.now()
	timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

	Datafile = os.path.expanduser(Datafile)
	Errorfile = os.path.expanduser(Errorfile)
	
	try:
		with open(Datafile, "a") as f:
			f.write(f"{timestamp}: {data}\n")
			print("writeSD done")
	except:
		with open(Errorfile, "a") as f:
			f.write(f"{timestamp}: Error Occurred\n")
			print("writeSD failed")
	return 


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

start = time.time()
while True:
	now = time.time() - start

	# CO2濃度取得
	co2_data = f"{read_co2()} ppm"


	Datafile = "~/Data/DataPath/log.txt"
	Errorfile = "~/Data/ErrorPath/log.txt"

	writeSD(Datafile, Errorfile, co2_data)
	
	if now > 24 * 60 * 60 :
		break
	time.sleep(16)