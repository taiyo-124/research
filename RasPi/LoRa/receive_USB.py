"""
USBタイプのLora通信モジュールを用いる際のコード

"""


import serial
import time

# 引数でポートを指定するように変更
def main(ser_receive):
    data_received = ser_receive.read(200)
    print(data_received)

    time.sleep(1)
    if len(data_received) != 0:
        high = data_received[0]
        low = data_received[1]
        co2 = (high << 8) | low
        ser_receive.flush()
        return co2
    else:
        return None
        
ser_receive = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

while True:
    receive_co2 = main(ser_receive)
    if receive_co2 is None:
        continue
    else:
        print(f"CO₂ 濃度: {receive_co2} ppm")

