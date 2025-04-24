import serial
import time



def main():
    # ポート設定
    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )

    # Hello Worldを送信: 2byte(宛先デバイスアドレス) 1byte(待受周波数チャネル)
    payload = bytes([0x00, 0x00, 0x00, 0x68, 0x65, 0x6C, 0x6C, 0x6F])

    ser.write(payload)
    ser.flush()
    print("SENDED")
    time.sleep(1)
    return 

while True:
    main()