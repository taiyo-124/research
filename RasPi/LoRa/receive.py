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

    data_received = ser.read(8)
    print(len(data_received))
    print(data_received[0:5])
    ser.flush()
    time.sleep(1)
    return

while True:
    main()
