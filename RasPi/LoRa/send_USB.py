"""
USBタイプのLora通信モジュールを用いる際のコード

"""

import serial
import time



def main():

    # CO2濃度をセンサから取得
    # センサ側のポートを設定
    ser_sense = serial.Serial(
        port='/dev/ttyAMA4',
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )

    # CO₂ 濃度取得コマンド [SlaveAdd, FuncCode, StartAdd(Up), StartAdd(Down), NumRegister(Up), NumRegister(Down)], CRC, CRC]
    # 0x68のデバイスから03アドレスのレジスタ1個のデータを取得するコマンド
    get_command = bytearray([0X68, 0x04, 0x00, 0x03, 0x00, 0x01, 0xC8, 0xF3])
    ser_sense.write(get_command)
    time.sleep(0.1)

    # response[0x68(省略), 0x04, bytecount, Register value(Up), Register value(Down), CRC, CRC]
    response_co2 = ser_sense.read(7)
    # print(response_co2)
    high = response_co2[3]
    low = response_co2[4]
    co2 = (high << 8) | low
    print(f"CO2濃度: {co2}ppm")
    
    ser_sense.flush()

    # LoRaで取得したCO2濃度を送信
    # 通信モジュールのポート設定
    ser_send = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )

    # 2byte(宛先デバイスアドレス) 1byte(待受周波数チャネル)どちらも0
    payload = bytes([0x00, 0x00, 0x00, high, low])  
    ser_send.write(payload)
    ser_send.flush()
    print("Data sended")
    return

while True:
    main()
    # CO2センサのデフォルトセンシング間隔が16sなので16秒待つ
    time.sleep(60)