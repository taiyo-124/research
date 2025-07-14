import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.ticker as ticker
import matplotlib.dates as mdates


"""
以下に, データ分析の詳細

時間と電圧値のグラフ

"""


# データ読み込み(~/Data/以下指定) "file_間隔"で指定
df_list = []

file_10SEC = 'CPUSleep/10SEC.csv'
df_10SEC = pd.read_csv(f'/home/kawashima/Data/{file_10SEC}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
df_list.append(df_10SEC)

file_1MIN = 'CPUSleep/1MIN.csv'
df_1MIN = pd.read_csv(f'/home/kawashima/Data/{file_1MIN}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
df_list.append(df_1MIN)

file_2MIN = 'CPUSleep/2MIN.csv'
df_2MIN = pd.read_csv(f'/home/kawashima/Data/{file_2MIN}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
df_list.append(df_2MIN)

file_10MIN = 'CPUSleep/10MIN.csv'
df_10MIN = pd.read_csv(f'/home/kawashima/Data/{file_10MIN}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
df_list.append(df_10MIN)


print(df_list)



""" 以下, RasPi側でデータを取得したときに実行(df.index: %H:%M:%S) """

# indexを時刻から動作時間に変換 (その際必要に応じて'voltage'の平均化を行う)
for df in df_list:
    df.index = pd.to_datetime(df.index)
    elapsed_s = (df.index - df.index[0])
    df.index = pd.to_timedelta(elapsed_s, unit='s')
    df.index = df.index.total_seconds() / 60 / 60
    print(df)

df_10SEC['voltage'] = df_10SEC.groupby(np.arange(len(df_10SEC)) // 5)['voltage'].transform('mean')
df_1MIN['voltage'] = df_1MIN.groupby(np.arange(len(df_1MIN)) // 4)['voltage'].transform('mean')
df_2MIN['voltage'] = df_2MIN.groupby(np.arange(len(df_2MIN)) // 3)['voltage'].transform('mean')
    # # 'voltage'の平均化
    # df['voltage'] = df.groupby(np.arange(len(df)) // (group_size))['voltage'].transform('mean')


""" 以下, 行いたい操作を記述 """

# 経過時間と電圧のグラフを表示
print("Plot Beginning")


plt.figure(figsize=(10, 5))
plt.plot(df_10SEC.index, df_10SEC['voltage'], label='10 sec')
plt.plot(df_1MIN.index, df_1MIN['voltage'], label='1 min')
plt.plot(df_2MIN.index, df_2MIN['voltage'], label='2 min')
plt.plot(df_10MIN.index, df_10MIN['voltage'], label='10 min')


plt.xlabel("Operation Duration (hour)")
plt.ylabel("Voltage (mV)")
plt.title("Voltage Variation")
plt.grid(True)
plt.legend(fontsize=15)


# 目盛りを1刻みに
ax = plt.gca()
ax.tick_params(which='minor', direction='in')
ax.tick_params(which='major', length=5, direction='in')
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.set_xlim(left=0, right=34)
ax.set_ylim(bottom=3300)


plt.show()