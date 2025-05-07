"""
USBタイプのLora通信モジュールを用いる際のコード

"""


import serial
import time

# 引数でポートを指定するように変更
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


