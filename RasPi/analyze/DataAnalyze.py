import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates


"""
以下に, データ分析の詳細

電圧値とRSSIのグラフ

"""


# データ読み込み(~/Data/以下指定)
file_DeepSleep = 'LoRa/1MINDeepSleepLoRa.csv'
df_DeepSleep = pd.read_csv(f'/home/kawashima/Data/{file_DeepSleep}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])

file_Normal = 'LoRa/1MINLoRa.csv'
df_Normal = pd.read_csv(f'/home/kawashima/Data/{file_Normal}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])

file_SD = 'SDCard/1MINSD.csv'
df_SD = pd.read_csv(f'/home/kawashima/Data/{file_SD}', index_col=0, skiprows=3, names=["temperature", "humidity", "pressure", "voltage"])


""" 以下, RasPi側でデータを取得したときに実行(df.index: %H:%M:%S) """
# 電圧値を5分単位で平均化
group_size = 5

# RSSIで条件をつけて有効なデータを取り出す
df_DeepSleep_valid = df_DeepSleep[df_DeepSleep['RSSI'] > -100]

# indexを経過時間に変換(Timedelta型)
df_DeepSleep_valid.index = pd.to_datetime(df_DeepSleep_valid.index)
elapsed_s_LoRa = (df_DeepSleep_valid.index - df_DeepSleep_valid.index[0])
df_DeepSleep_valid.index = pd.to_timedelta(elapsed_s_LoRa, unit='s')

# さらにTimedelta型を時間単位に
df_DeepSleep_valid.index = df_DeepSleep_valid.index.total_seconds() / 60 / 60 

# 'voltage'の平均化
df_DeepSleep_valid['voltage'] = df_DeepSleep_valid.groupby(np.arange(len(df_DeepSleep_valid)) // group_size)['voltage'].transform('mean')
print(df_DeepSleep_valid)


df_Normal_valid = df_Normal[df_Normal['RSSI'] > -100]
# 経過時間に変換(Timedelta型)
df_Normal_valid.index = pd.to_datetime(df_Normal_valid.index)
elapsed_s_LoRa = (df_Normal_valid.index - df_Normal_valid.index[0])
df_Normal_valid.index = pd.to_timedelta(elapsed_s_LoRa, unit='s')
# Timedelta型を時間単位に
df_Normal_valid.index = df_Normal_valid.index.total_seconds() / 60 / 60 

# 'voltage'の平均化
df_Normal_valid['voltage'] = df_Normal_valid.groupby(np.arange(len(df_Normal_valid)) // group_size)['voltage'].transform('mean')
print(df_Normal_valid)



# """ 以下, Arduino側でデータを取得したときに実行(df.index: millis()) """

# df.indexを経過時間(単位:s)に変換
elapsed_s_SD = (df_SD.index - df_SD.index[0]) / 1000
df_SD.index = pd.to_timedelta(elapsed_s_SD, unit='s')
# Timedelta型を時間単位に
df_SD.index = df_SD.index.total_seconds() / 60 / 60 

# 'voltage'の平均化
df_SD['voltage'] = df_SD.groupby(np.arange(len(df_SD)) // group_size)['voltage'].transform('mean')
print(df_SD)


""" 以下, 行いたい操作を記述 """

# 経過時間と電圧のグラフを表示

plt.figure(figsize=(10, 5))
plt.plot(df_DeepSleep_valid.index, df_DeepSleep_valid['voltage'], color='r', label='DeepSleep LoRa')
plt.plot(df_SD.index, df_SD['voltage'], color='c', label='SD Card')
plt.plot(df_Normal_valid.index, df_Normal_valid['voltage'], color='orange', label='Normal LoRa')


plt.xlabel("Elapsed Time [hour]")
plt.ylabel("Voltage [mV]")
plt.title("Voltage Variation(interval 1min): LoRa(DeepSleep) vs LoRa(Normal) vs SD Card")
plt.grid(True)
plt.legend(fontsize=15, loc='upper right')




ax = plt.gca()

# テキストを追加(見栄え)
plt.axvline(x=9.369444, color='orange', linestyle='--', linewidth=1)
ax.text(9.5, 3330, "9h22m", color='orange')

plt.axvline(x=20.579984, color='c', linestyle='--', linewidth=1)
ax.text(20.7, 3330, "20h35m", color='c')

plt.axvline(x=27.415278, color='r', linestyle='--', linewidth=1)
ax.text(26, 3330, "27h25m", color='r')

# 目盛りを1刻みに
ax.tick_params(which='minor', direction='in')
ax.tick_params(which='major', length=5, direction='in')
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.set_xlim(left=0, right=28)
ax.set_ylim(bottom=3300)

plt.tight_layout()
plt.show()