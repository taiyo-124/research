import numpy as np
import pandas as pd

from datetime import datetime, timedelta

# 日付.csvファイルを前処理. 1回の測定結果を1つのcsvファイルにまとめる. 複数日にまたがっている⇛ MultiDate = True
MultiDate = True
date = '2025-06-17'
fileName = 'LoRa/5SECDeepSleepLoRa.csv'

# ファイルを読み込んでDataFrame化(その際にindexを日時に変更)
df_date1 = pd.read_csv(f'/home/kawashima/Data/RawData/{date}.csv', index_col=0, skiprows=2, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
print(df_date1.index)
df_date1.index = pd.to_datetime(df_date1.index)
# df_date1 = df_date1[df_date1.index.time >= pd.to_datetime("18:33:56").time()]

if MultiDate:
    dt1 = datetime.strptime(date, "%Y-%m-%d")
    dt2 = dt1 + timedelta(days=1)
    date2 = dt2.strftime("%Y-%m-%d")
    date_list = [date, date2]

    df_date2 = pd.read_csv(f'/home/kawashima/Data/RawData/{date2}.csv', index_col=0, skiprows=2, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])

    merged_df = pd.concat([df_date1, df_date2], axis=0)
    print(merged_df)

    merged_df.to_csv(f'/home/kawashima/Data/{fileName}', index=True)

else:
    df_date1.to_csv(f'/home/kawashima/Data/{fileName}', index=True)