import numpy as np
import pandas as pd

from datetime import datetime, timedelta

# 日付.csvファイルを前処理. 1回の測定結果を1つのcsvファイルにまとめる. 複数日にまたがっている ⇛ またがっている日数 = NumDates
NumDates = 1
date = '2025-05-14'
fileName = 'NoSleep/1MIN.csv'

# ファイルを読み込んでDataFrame化(その際にindexを日時に変更)
df_origin = pd.read_csv(f'/home/kawashima/Data/RawData/{date}.csv', index_col=0, skiprows=2, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
print(df_origin.index)
df_origin.index = pd.to_datetime(df_origin.index)

# 不要データを除いて前処理したいとき
df_origin = df_origin[df_origin.index.time <= pd.to_datetime("20:20:00").time()]
date_list = [date]

# マージ
for i in range (1, NumDates):
    # 日付取得
    dt_origin = datetime.strptime(date, "%Y-%m-%d")
    dt_next = dt_origin + timedelta(days=i)
    date_next = dt_next.strftime("%Y-%m-%d")


    date_list.append(date_next)
    print(date_list)


    df_date_next = pd.read_csv(f'/home/kawashima/Data/RawData/{date_next}.csv', index_col=0, skiprows=2, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
    # マージしてdf_originを置き換え
    df_origin = pd.concat([df_origin, df_date_next], axis=0)

# CSVファイルとして保存
df_origin.to_csv(f'/home/kawashima/Data/{fileName}', index=True)