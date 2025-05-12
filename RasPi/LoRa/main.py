# main関数
import os
import serial
import time
import struct
from datetime import datetime
import pandas as pd


# ポート設定 (使用するLoraモジュールによって使い分ける: USBとGPIO)
ser_USB = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

ser_GPIO = serial.Serial(
    port='/dev/ttyAMA2',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)


# 引数はシリアルポートのみ: USBを使用
def main(ser):
    while True:
        # データ読み込み
        received_data = reading_ser(ser)
        if received_data is None:
            continue
        
        # nullバイト除去
        print(f"受信バイト: {len(received_data)}") # clean_dataは前から順に: 温度(4byte), 湿度(4byte), 気圧(4byte), 最終バイトはRSSI (後々変更される可能性大)

        if len(received_data) < 17:
            print(f"データが不正です")
            print("======================================================")
            continue

        # 現在時刻取得
        now = datetime.now()
        print(now)

        # 温度に戻す処理 (4byte⇛float)
        temperature = struct.unpack('<f', received_data[:4])[0]

        # 湿度に戻す処理 (4byte⇛float)
        humid = struct.unpack('<f', received_data[4:8])[0]

        # 気圧に戻す処理 (4byte⇛float)
        pressure = struct.unpack('<f', received_data[8:12])[0]

        # 電圧値(4byte⇛float)
        voltage = struct.unpack('<f', received_data[12:16])[0]

        # RSSI 
        RSSI = - (256 - received_data[-1])


        # 日時取得
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        csv_path = f"~/Data/LoRa/{date}.csv"

        # ~をhomeディレクトリとして認識させる
        csv_path = os.path.expanduser(csv_path)

        save_csv(csv_path, time, temperature, humid, pressure, voltage, RSSI)

        print("=============================================================================================")


# シリアルポートからデータを読み込み
def reading_ser(ser_receive):
    while(ser_receive.in_waiting == 0):
        time.sleep(0.1)
        pass
    
    time.sleep(0.5)
    
    bytes_available = ser_receive.in_waiting
    received_data = ser_receive.read(bytes_available)
    print(f"受信バイト: {bytes_available}")
    if len(received_data) != 0:
        return received_data
    else:
        return None


# csvファイルに保存(ファイルがなければ生成する)
def save_csv(path, time, temperature, humid, pressure, voltage, RSSI):
    # ファイル初期化
    if not os.path.exists(path):
        df_init = pd.DataFrame(index= [time], columns=["temperature", "humidity", "pressure", "voltage", "RSSI"])
        df_init.to_csv(path)

    df = pd.DataFrame([{
        "temperature": temperature,
        "humidity": humid,
        "pressure": pressure,
        "voltage": voltage,
        "RSSI": RSSI
    }], index=[time])
    
    #小数第２位までに丸める
    df = df.round(2)

    print(f"[{time}] 気温: {temperature:.2f}℃, 湿度: {humid:.2f}%, 気圧: {pressure:.2f}kPa, 電圧: {voltage:.3f}mV, RSSI: {RSSI}dBm")

    # csvファイルに追記保存
    df.to_csv(path, mode='a', header=False)

    return
    

if __name__ == "__main__":
    main(ser_USB)