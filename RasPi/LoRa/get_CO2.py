# CO2濃度をセンサから取得する

import serial
import time

ser_sense = serial.Serial(
    port='/dev/ttyAMA4',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

# ポート設定を引数
def sense(ser_sense):
    # CO₂ 濃度取得コマンド [SlaveAdd, FuncCode, StartAdd(Up), StartAdd(Down), NumRegister(Up), NumRegister(Down)], CRC, CRC]
    # 0x68のデバイスから03アドレスのレジスタ1個のデータを取得するコマンド
    get_command = bytearray([0X68, 0x04, 0x00, 0x03, 0x00, 0x01, 0xC8, 0xF3])
    ser_sense.write(get_command)
    time.sleep(0.1)

    # response[0x68(省略), 0x04, bytecount, Register value(Up), Register value(Down), CRC, CRC]
    response_co2 = ser_sense.read(7)
    high = response_co2[3]
    low = response_co2[4]
    return high, low

# # 確認用コード
# while True:
#     high, low = get_CO2(ser_sense)
#     co2 = (high << 8) | low
#     print(f"CO2濃度: {co2}ppm")
#     time.sleep(16)