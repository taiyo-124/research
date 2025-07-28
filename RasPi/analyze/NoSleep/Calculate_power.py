import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib.patches as patches
import matplotlib.ticker as ticker
import matplotlib.dates as mdates

# 1. データ前処理

df_list = []


file_2SEC = 'LoRa/2SECDeepSleepLoRa.csv'
df_2SEC = pd.read_csv(f'/home/kawashima/Data/{file_2SEC}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
df_list.append(df_2SEC)

file_5SEC = 'LoRa/5SECDeepSleepLoRa.csv'
df_5SEC = pd.read_csv(f'/home/kawashima/Data/{file_5SEC}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
df_list.append(df_5SEC)

file_10SEC = 'LoRa/10SECDeepSleepLoRa_v2.csv'
df_10SEC = pd.read_csv(f'/home/kawashima/Data/{file_10SEC}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
df_list.append(df_10SEC)


file_30SEC = 'LoRa/30SECDeepSleepLoRa.csv'
df_30SEC = pd.read_csv(f'/home/kawashima/Data/{file_30SEC}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
df_list.append(df_30SEC)

file_1MIN = 'NoSleep/1MIN.csv'
df_1MIN = pd.read_csv(f'/home/kawashima/Data/{file_1MIN}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
df_list.append(df_1MIN)

# 経過時間のリスト
elapsed_time_list = []
# indexを経過時間(min)に変換
for df in df_list:
    df.index = pd.to_datetime(df.index)
    elapsed_s_1SEC = (df.index - df.index[0])
    df.index = pd.to_timedelta(elapsed_s_1SEC, unit='s')
    df.index = df.index.total_seconds() / 60 
    print(df.index[-1])
    elapsed_time_list.append(df.index[-1])
print(elapsed_time_list)

# 時間間隔のリスト 
span_list = np.array([2, 5, 10, 30, 60])
span_list_min = span_list / 60
print(span_list)

x = 1 / span_list_min
elapsed_time_list = np.array(elapsed_time_list)
y = 1 / elapsed_time_list

# --- 3. Model Fitting (using numpy.polyfit) ---

# Case 1: Using all data
# np.polyfit(x, y, 1) returns coefficients [slope, intercept]
slope, intercept = np.polyfit(x, y, 1)
ratio_val = slope / intercept
power_ratio= 1 / (1 / ratio_val)
print("===== NoSleep =====")
print(f"動的電力: {slope}, 静的電力: {intercept}, 比={slope/intercept}")


# x軸とy軸をもとに戻してplot
plt.figure(figsize=(12, 6))
x_fit = np.linspace(0.01, 10.5, 100)
y_fit = 1 / (slope / x_fit + intercept)

ax = plt.gca()
ax.tick_params(which='minor', direction='in')
ax.tick_params(which='major', length=5, direction='in')
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
plt.scatter(span_list_min, elapsed_time_list, color='blue', label='Data')
ax.plot(x_fit, y_fit, color='green', linestyle='--', label='Estimated Time')

ax.set_xlim(0, max(x_fit) )
ax.set_ylim(0, 2150)
ax.set_xlabel('Interval (min)')
ax.set_ylabel('Operation Time (min)')

plt.grid(True)
plt.legend(fontsize=15, loc='lower right')
plt.show()