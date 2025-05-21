import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates


# データ読み込み(~/Data/以下指定)
fileSD = 'SDCard/1MinSD.csv'
df_SD = pd.read_csv(f'/home/kawashima/Data/{fileSD}', index_col=0, skiprows=3, names=["temperature", "humidity", "pressure", "voltage"])

fileLoRa = 'LoRa/1MINLoRa.csv'
df_LoRa = pd.read_csv(f'/home/kawashima/Data/{fileLoRa}', index_col=0)
print(df_LoRa)


""" 以下, RasPi側でデータを取得したときに実行(df.index: %H:%M:%S) """

# RSSIで条件をつけてデータを取り出す
df_LoRa_valid = df_LoRa[df_LoRa['RSSI'] > -100]

# 経過時間に変換(Timedelta型)
df_LoRa_valid.index = pd.to_datetime(df_LoRa_valid.index)
elapsed_s_LoRa = (df_LoRa_valid.index - df_LoRa_valid.index[0])
df_LoRa_valid.index = pd.to_timedelta(elapsed_s_LoRa, unit='s')
# Timedelta型を時間単位に
df_LoRa_valid.index = df_LoRa_valid.index.total_seconds() / 60 / 60 
print(df_LoRa_valid)



""" 以下, Arduino側でデータを取得したときに実行(df.index: millis()) """

# df.indexを経過時間(単位:s)に変換
elapsed_s_SD = (df_SD.index - df_SD.index[0]) / 1000
df_SD.index = pd.to_timedelta(elapsed_s_SD, unit='s')
# Timedelta型を時間単位に
df_SD.index = df_SD.index.total_seconds() / 60 / 60 
print(df_SD)


""" 以下, 行いたい操作を記述 """

# 経過時間と電圧のグラフを表示

plt.figure(figsize=(10, 5))
plt.plot(df_SD.index, df_SD['voltage'], label="SD Card")
plt.plot(df_LoRa_valid.index, df_LoRa_valid['voltage'], label="LoRa")

plt.xlabel("Elapsed Time [hour]")
plt.ylabel("Voltage [mV]")
plt.title("Voltage Variation Comparison: SD Card vs LoRa")
plt.grid(True)
plt.legend(fontsize=18)

# 目盛りを1刻みに
ax = plt.gca()
ax.tick_params(which='minor', direction='in')
ax.tick_params(which='major', length=5, direction='in')
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.set_xlim(left=0, right=21)
ax.set_ylim(bottom=3300)

plt.tight_layout()
plt.show()