"""
USBタイプのLora通信モジュールを用いる際のコード

"""


import serial
import time
import struct
from datetime import datetime

# 引数でポートを指定するように変更
def reading_ser(ser_receive):
    while(ser_receive.in_waiting == 0):
        pass
    time.sleep(1)
    
    bytes_available = ser_receive.in_waiting
    received_data = ser_receive.read(bytes_available)
    print(f"受信バイト: {bytes_available}")
    if len(received_data) != 0:
        return received_data
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
    # 受信データがあるかどうかを確認
    if ser_receive.in_waiting == 0:
        continue
    else:
        time.sleep(1) # 完全な受信データを取得するために少し待つ

        # 時刻取得
        now = datetime.now()
        print(now)

        # データ読み込み
        received_data = reading_ser(ser_receive)

        # nullバイトを除去
        clean_data = received_data.replace(b'\x00', b'')
        print(f"有効バイト: {len(clean_data)}") # clean_dataは前から順に: 温度(4byte), 湿度(4byte), 気圧(4byte), 最終バイトはRSSI

        # 温度に戻す処理
        temperature = struct.unpack('<f', clean_data[:4])[0]
        print(f"気温: {temperature:.2f}[℃]")

        # 湿度に戻す処理
        humid = struct.unpack('<f', clean_data[4:8])[0]
        print(f"湿度: {humid:.2f}[%]")

        # 気圧に戻す処理
        pressure = struct.unpack('<f', clean_data[8:12])[0]
        print(f"気圧: {pressure:.2f}[kPa]")

        # RSSI
        RSSI = - (256 - clean_data[-1])
        print(f"RSSI: {RSSI}[dBm]")

        print("=========================================================\n")

