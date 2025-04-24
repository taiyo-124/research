import serial
import time 




def config():
    # ポート設定
    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )

    # Modeが4種類ある(Normal, WORTransmit, WORReceive, Config/Deepsleep)
    # 今回はconfig設定のため, mode3

    # コマンドフォーマット[c0, staring address, length, parameters]

    request = bytearray([0XC0, 0X00, 0X08, 0X00, 0X00, 0X70, 0X01, 0X00, 0XC5, 0X00, 0X00])
    # 0xc0: レジスタ値の書き込みコマンド
    # 0x00: 開始アドレス
    # 0x08: 8アドレスに書き込み(後ろに8コマンド続く)
    # 0x00 0x00: Module Address (default)
    # 0x70: BW, SFを設定(0111 0000)
    # 0x01; パケット長と送信出力電力(00, reserved000, 01)
    # 0x00: 周波数チャネルを0に設定
    # 0xc5: 1100 0101→RSSIバイト有効化, 固定送信モード, reserved(3bit), WORサイクルを3000msに設定
    # 0x00 0x00: 暗号キーを0に設定

    ser.write(request)
    time.sleep(0.1)
    response = ser.read(11)
    ser.close()

    return response

def check():
    # ポート設定
    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )
    request = bytearray([0xC1, 0x00, 0x08])
    ser.write(request)
    time.sleep(1)
    response = ser.read(11)
    return response



print(config())
print(check())