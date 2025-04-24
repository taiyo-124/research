import serial
import time

def main():
    # ポート設定
    ser_receive = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )

    data_received = ser_receive.read(5)
    print(len(data_received))
    ser_receive.flush()
    time.sleep(1)
    high = data_received[3]
    low = data_received[4]
    return high, low

while True:
    high, low = main()
    co2 = (high << 8) | low
    print(f"CO₂ 濃度: {co2} ppm")
