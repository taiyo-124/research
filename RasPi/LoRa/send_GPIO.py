"""
GPIOタイプのLora通信モジュールを用いるコード

GPIO 0と1を用いてポートは/dev/ttyAMA2に接続していることを確認
$pinctl get, $pinoutで確認可能
"""

import serial 
import time 

import get_CO2

# CO2センサ用ポート設定
ser_sense = serial.Serial(
    port='/dev/ttyAMA4',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

# Lora通信用ポート設定
ser_send = serial.Serial(
    port='/dev/ttyAMA2',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

# high, low: CO2濃度センサから取得する値
def send_GPIO(ser_send, high, low):

    payload = bytes([0x00, 0x00, 0x00, high, low])  
    ser_send.write(payload)
    ser_send.flush()
    print("Data sended")
    return

while True:
    high, low = get_CO2.sense(ser_sense)
    send_GPIO(ser_send, high, low)
    time.sleep(16)
