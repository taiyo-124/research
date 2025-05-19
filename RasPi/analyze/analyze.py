import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# データ読み込み(日付で指定)
date = '2025-05-14'
df = pd.read_csv(f'/home/kawashima/Data/LoRa/{date}.csv', index_col=0, skiprows=2, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])

# df.indexを完全な日時に変換するためのコード(保存の際に変に日時情報を落として保存しているために必要となる. 要改善)
df.index = pd.to_datetime(df.index, format='%H:%M:%S')
date_only = pd.to_datetime(date)
df.index = df.index.map(lambda dt: pd.Timestamp.combine(date_only.date(), dt.time()))

# RSSIで条件をつけてデータを取り出す
df_valid = df[df['RSSI'] > -100]

plt.figure(figsize=(10, 5))
plt.plot(df_valid.index, df_valid['voltage'])
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.xlabel('Time')
plt.ylabel('Voltage')
plt.title(f'Voltage over Time on {date}')
plt.grid(True)
plt.savefig(f'figs/Voltage over Time on {date}')