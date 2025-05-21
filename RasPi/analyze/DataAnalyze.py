import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates


# データ読み込み(~/Data/以下指定)
file1 = 'LoRa/1MINLoRa.csv'
df_LoRa1 = pd.read_csv(f'/home/kawashima/Data/{file1}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])

file2 = 'LoRa/2MINLoRa.csv'
df_LoRa2 = pd.read_csv(f'/home/kawashima/Data/{file2}', index_col=0, skiprows=3, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
print(df_LoRa2)


""" 以下, RasPi側でデータを取得したときに実行(df.index: %H:%M:%S) """

# RSSIで条件をつけてデータを取り出す
df_LoRa_valid = df_LoRa1[df_LoRa1['RSSI'] > -100]

# 経過時間に変換(Timedelta型)
df_LoRa_valid.index = pd.to_datetime(df_LoRa_valid.index)
elapsed_s_LoRa = (df_LoRa_valid.index - df_LoRa_valid.index[0])
df_LoRa_valid.index = pd.to_timedelta(elapsed_s_LoRa, unit='s')
# Timedelta型を時間単位に
df_LoRa_valid.index = df_LoRa_valid.index.total_seconds() / 60 / 60 
print(df_LoRa_valid)

df_LoRa2.index = pd.to_datetime(df_LoRa2.index)
elapsed_s_LoRa2 = (df_LoRa2.index - df_LoRa2.index[0])
df_LoRa2.index = pd.to_timedelta(elapsed_s_LoRa2, unit='s')
df_LoRa2.index = df_LoRa2.index.total_seconds() / 60 / 60
print(df_LoRa2)



# """ 以下, Arduino側でデータを取得したときに実行(df.index: millis()) """

# # df.indexを経過時間(単位:s)に変換
# elapsed_s_SD = (df_SD.index - df_SD.index[0]) / 1000
# df_SD.index = pd.to_timedelta(elapsed_s_SD, unit='s')
# # Timedelta型を時間単位に
# df_SD.index = df_SD.index.total_seconds() / 60 / 60 
# print(df_SD)


""" 以下, 行いたい操作を記述 """

# 経過時間と電圧のグラフを表示

plt.figure(figsize=(10, 5))
plt.plot(df_LoRa_valid.index, df_LoRa_valid['voltage'], label="Interval: 1 minute")
plt.plot(df_LoRa2.index, df_LoRa2['voltage'], label="Interval: 2 minute")

plt.xlabel("Elapsed Time [hour]")
plt.ylabel("Voltage [mV]")
plt.title("Voltage Variation During LoRa: 1 minute vs 2 minute")
plt.grid(True)
plt.legend(fontsize=15)

# 目盛りを1刻みに
ax = plt.gca()
ax.tick_params(which='minor', direction='in')
ax.tick_params(which='major', length=5, direction='in')
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.set_xlim(left=0, right=9.5)
ax.set_ylim(bottom=3300)

plt.tight_layout()
plt.show()