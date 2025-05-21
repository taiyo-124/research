import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates


# データ読み込み(~/Data/以下指定)
fileSD = 'SDCard/1MinSD.csv'
df_SD = pd.read_csv(f'/home/kawashima/Data/{fileSD}', index_col=0, skiprows=3, names=["temperature", "humidity", "pressure", "voltage"])

fileLoRa = 'LoRa/'


""" 以下, RasPi側でデータを取得したときに実行(df.index: %H:%M:%S) """

# # df.indexを完全な日時に変換するためのコード(保存の際に変に日時情報を落として保存しているために必要となる. 要改善)
# df.index = pd.to_datetime(df.index, format='%H:%M:%S')
# date_only = pd.to_datetime(date)
# df.index = df.index.map(lambda dt: pd.Timestamp.combine(date_only.date(), dt.time()))
# # RSSIで条件をつけてデータを取り出す
# df_valid = df[df['RSSI'] > -100]


""" 以下, Arduino側でデータを取得したときに実行(df.index: millis()) """

# df.indexを経過時間(単位:s)に変換
elapsed_s = (df_SD.index - df_SD.index[0]) / 1000
df_SD.index = pd.to_timedelta(elapsed_s, unit='s')
# Timedelta型を時間単位に
df_SD.index = df_SD.index.total_seconds() / 60 / 60 
print(df_SD)


""" 以下, 行いたい操作を記述 """

# 経過時間と電圧のグラフを表示

plt.figure(figsize=(10, 5))
plt.plot(df.index, df['voltage'])

plt.xlabel("Elapsed Time")
plt.ylabel("Voltage")
plt.title("Voltage Varation During Saving to SD Card")
plt.grid(True)

# 目盛りを1時間刻みに
ax = plt.gca()
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.set_xlim(left=0, right=21)

plt.tight_layout()
plt.show()