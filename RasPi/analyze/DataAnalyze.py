import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates


"""
以下に, データ分析の詳細

電圧値とRSSIのグラフ

"""


# データ読み込み(~/Data/以下指定) "file_間隔"で指定
#
file_1MIN = 'LoRa/1MINDeepSleepLoRa.csv'
df_1MIN = pd.read_csv(f'/home/kawashima/Data/{file_1MIN}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
print(df_1MIN)
print(len(df_1MIN))

file_1SEC = 'LoRa/1SECDeepSleepLoRa.csv'
df_1SEC = pd.read_csv(f'/home/kawashima/Data/{file_1SEC}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
print(df_1SEC)
print(len(df_1SEC))


""" 以下, RasPi側でデータを取得したときに実行(df.index: %H:%M:%S) """
# 電圧値を3つ単位で平均化
group_size_1MIN = 5
group_size_1SEC = 5

# RSSIで条件をつけてデータを取り出す
df_1MIN = df_1MIN[df_1MIN['RSSI'] > -100]

# 経過時間に変換(Timedelta型)
df_1MIN.index = pd.to_datetime(df_1MIN.index)
elapsed_s_1MIN = (df_1MIN.index - df_1MIN.index[0])
df_1MIN.index = pd.to_timedelta(elapsed_s_1MIN, unit='s')
# Timedelta型を時間単位に
df_1MIN.index = df_1MIN.index.total_seconds() / 60 / 60 
print(df_1MIN)

df_1SEC.index = pd.to_datetime(df_1SEC.index)
elapsed_s_1SEC = (df_1SEC.index - df_1SEC.index[0])
df_1SEC.index = pd.to_timedelta(elapsed_s_1SEC, unit='s')
df_1SEC.index = df_1SEC.index.total_seconds() / 60 / 60
print(df_1SEC)

# 'voltage'の平均化
df_1MIN['voltage'] = df_1MIN.groupby(np.arange(len(df_1MIN)) // (group_size_1MIN))['voltage'].transform('mean')
print(df_1MIN)

# 'voltage'の平均化
df_1SEC['voltage'] = df_1SEC.groupby(np.arange(len(df_1SEC)) // group_size_1SEC)['voltage'].transform('mean')
print(df_1SEC)



# """ 以下, Arduino側でデータを取得したときに実行(df.index: millis()) """

# # df.indexを経過時間(単位:s)に変換
# elapsed_s_SD = (df_SD.index - df_SD.index[0]) / 1000
# df_SD.index = pd.to_timedelta(elapsed_s_SD, unit='s')
# # Timedelta型を時間単位に
# df_SD.index = df_SD.index.total_seconds() / 60 / 60 

# # 'voltage'の平均化
# df_SD['voltage'] = df_SD.groupby(np.arange(len(df_SD)) // group_size)['voltage'].transform('mean')
# print(df_SD)


""" 以下, 行いたい操作を記述 """

# 経過時間と電圧のグラフを表示

plt.figure(figsize=(10, 5))
plt.plot(df_1MIN.index, df_1MIN['voltage'], label="DeepSleep 1 Min")
plt.plot(df_1SEC.index, df_1SEC['voltage'], label="DeepSleep 1 Sec")


plt.xlabel("Elapsed Time [hour]")
plt.ylabel("Voltage [mV]")
# plt.title("Voltage Variation DeepSleep 1 Min vs DeepSleep 1 SEC")
plt.grid(True)
plt.legend(fontsize=15)


# 目盛りを1刻みに
ax = plt.gca()
ax.tick_params(which='minor', direction='in')
ax.tick_params(which='major', length=5, direction='in')
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.set_xlim(left=0)
ax.set_ylim(bottom=3300)

plt.tight_layout()
plt.show()