import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.ticker as ticker
import matplotlib.dates as mdates


"""
以下に, データ分析の詳細

電圧値とRSSIのグラフ

"""


# データ読み込み(~/Data/以下指定) "file_間隔"で指定
df_list = []

file_1SEC = 'LoRa/1SECDeepSleepLoRa.csv'
df_1SEC = pd.read_csv(f'/home/kawashima/Data/{file_1SEC}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
df_list.append(df_1SEC)
print(df_1SEC)
print(len(df_1SEC))

file_2SEC = 'LoRa/2SECDeepSleepLoRa.csv'
df_2SEC = pd.read_csv(f'/home/kawashima/Data/{file_2SEC}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
df_list.append(df_2SEC)

file_5SEC = 'LoRa/5SECDeepSleepLoRa.csv'
df_5SEC = pd.read_csv(f'/home/kawashima/Data/{file_5SEC}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
df_list.append(df_5SEC)

file_10SEC = 'LoRa/10SECDeepSleepLoRa.csv'
df_10SEC = pd.read_csv(f'/home/kawashima/Data/{file_10SEC}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
df_list.append(df_10SEC)

file_10SEC_v2 = 'LoRa/10SECDeepSleepLoRa_v2.csv'
df_10SEC_v2 = pd.read_csv(f'/home/kawashima/Data/{file_10SEC_v2}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
df_list.append(df_10SEC_v2)

file_30SEC = 'LoRa/30SECDeepSleepLoRa.csv'
df_30SEC = pd.read_csv(f'/home/kawashima/Data/{file_30SEC}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
df_list.append(df_30SEC)

file_1MIN = 'LoRa/1MINDeepSleepLoRa.csv'
df_1MIN = pd.read_csv(f'/home/kawashima/Data/{file_1MIN}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])

# RSSIで条件をつけてデータを取り出す
df_1MIN = df_1MIN[df_1MIN['RSSI'] > -100]

df_list.append(df_1MIN)
print(df_1MIN)

print(df_list)

""" 以下, RasPi側でデータを取得したときに実行(df.index: %H:%M:%S) """
# 電圧値を3つ単位で平均化
group_size = 5
group_size_1MIN = 5
group_size_1SEC = 5
group_size_2SEC = 5
group_size_5SEC = 5

group_size_list = [5, 5, 5, 5]

for df in df_list:
    df.index = pd.to_datetime(df.index)
    elapsed_s = (df.index - df.index[0])
    df.index = pd.to_timedelta(elapsed_s, unit='s')
    df.index = df.index.total_seconds() / 60 / 60
    print(df)

    # 'voltage'の平均化
    df['voltage'] = df.groupby(np.arange(len(df)) // (group_size))['voltage'].transform('mean')



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
print("Plot Beginning")

plt.figure(figsize=(10, 5))
plt.plot(df_1SEC.index, df_1SEC['voltage'], label="1 sec")
plt.plot(df_2SEC.index, df_2SEC['voltage'], label="2 sec")
plt.plot(df_5SEC.index, df_5SEC['voltage'], label='5 sec')
plt.plot(df_10SEC.index, df_10SEC['voltage'], label='10 sec')
plt.plot(df_10SEC_v2.index, df_10SEC_v2['voltage'], label='10 sec v2')
plt.plot(df_30SEC.index, df_30SEC['voltage'], label='30 sec')
plt.plot(df_1MIN.index, df_1MIN['voltage'], label="1 min")


plt.xlabel("Elapsed Time (hour)")
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
ax.set_xlim(left=0)
ax.set_ylim(bottom=3300)

# 枠で囲む(グラフの変な部分)
rect_x = 5.05
rect_y = 3695
rect_width = 0.5
rect_height = 75
rect = patches.Rectangle((rect_x, rect_y), rect_width, rect_height,
                         edgecolor='black', facecolor='none',
                         linewidth=2, linestyle='--')

rect_x2 = 6.67
rect_y2 = 3825
rect2 = patches.Rectangle((rect_x2, rect_y2), rect_width, rect_height, edgecolor='black', facecolor='none', linewidth=2, linestyle='--')

rect_x3 = 9.49
rect_y3 = 3645
rect3 = patches.Rectangle((rect_x3, rect_y3), rect_width, 50, edgecolor='black', facecolor='none', linewidth=2, linestyle='--')
# パッチを追加
plt.gca().add_patch(rect)
plt.gca().add_patch(rect2)
plt.gca().add_patch(rect3)
# テキストを追加
plt.text(7, 3675, '???', fontsize=20, color='black')

plt.tight_layout()
plt.show()