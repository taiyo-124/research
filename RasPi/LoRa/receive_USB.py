"""
USBタイプのLora通信モジュールを用いる際のコード

"""


import serial
import time
import struct
from datetime import datetime

# 引数でポートを指定するように変更
<<<<<<< HEAD
def main(ser_receive, bytes_available):

    received_data = ser_receive.read(bytes_available)
    time.sleep(1)
    if len(received_data) != 0:
        return received_data
=======
def main(ser_receive):
    data_received = ser_receive.read(200)
    print(data_received, len(data_received))

    time.sleep(0.1)
    if len(data_received) != 0:
        high = data_received[0]
        low = data_received[1]
        co2 = (high << 8) | low

        RSSI = data_received[2]
        dBm = - (256 - RSSI)

        ser_receive.flush()

        return co2, dBm
>>>>>>> origin
    else:
        return None, None
        
ser_receive = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)


while True:
<<<<<<< HEAD
    # 受信データがあるかどうかを確認
    if ser_receive.in_waiting == 0:
        continue
    else:
        time.sleep(1) # 完全な受信データを取得するために少し待つ
=======
    
    receive_co2, dBm = main(ser_receive)

    if receive_co2 is None:
        continue
    else:
        print(f"CO₂ 濃度: {receive_co2} ppm")
        print(f"RSSI: {dBm} dBm")

    print("========================================")

    # # RSSI取得コマンド(開始アドレス: 00, 読み出しレジスタ数: 01)
    # RSSI_command = bytearray([0xC0, 0xC1, 0xC2, 0xC3, 0x00, 0x01])
    # ser_receive.write(RSSI_command)
    # time.sleep(0.1)
    # response_RSSI = ser_receive.read(4)
    # print(response_RSSI)

    # value_RSSI = []
    # value_RSSI.append(response_RSSI[-1])    

    # for value in value_RSSI:
    #     print(f"RSSI: {-(256 - value)}dBm ")

>>>>>>> origin

        # 時刻取得
        now = datetime.now()
        print(now)

        bytes_available = ser_receive.in_waiting
        print(f"受信バイト: {bytes_available}")
        received_data = main(ser_receive, bytes_available)

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

        print("=========================================================")
