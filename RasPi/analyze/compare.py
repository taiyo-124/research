import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib.patches as patches
import matplotlib.ticker as ticker
import matplotlib.dates as mdates


""" NoSleep """
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


""" CPUSleep """
# --- 1. Data Preparation ---
# Interval (minutes)
intervals = np.array([1/6, 1, 2, 10])
# Operating Time (hours, minutes)
durations_h = np.array([20, 30, 30, 33])
durations_m = np.array([19, 8, 57, 19])

# Convert all time units to minutes
total_minutes = durations_h * 60 + durations_m

# --- 2. Data Transformation for Linear Regression ---
# y = 1 / Operating Time
# x = 1 / Interval
x = 1 / intervals
y = 1 / total_minutes

# --- 3. Model Fitting (using numpy.polyfit) ---

# Case 1: Using all data
# np.polyfit(x, y, 1) returns coefficients [slope, intercept]
slope_CPUSleep, intercept_CPUSleep = np.polyfit(x, y, 1)


# Case 2: Excluding the suspicious outlier (the last data point)
slope_CPUSleep, intercept_CPUSleep = np.polyfit(x, y, 1)
ratio_val = slope_CPUSleep / intercept_CPUSleep
power_ratio= 1 / (1 / ratio_val)
print("===== CPUSleep =====")
print(f"動的電力: {slope_CPUSleep}, 静的電力: {intercept_CPUSleep}, 比={slope_CPUSleep/intercept_CPUSleep}")


# plot
plt.figure(figsize=(12, 6))
x_fit = np.linspace(0.01, 10.5, 100)
y_fit = 1 / (slope / x_fit + intercept)
print(y_fit)

ax = plt.gca()
ax.tick_params(which='minor', direction='in')
ax.tick_params(which='major', length=5, direction='in')
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())

# NoSleep plot
plt.scatter(span_list_min, elapsed_time_list, color='red', label='Data (No Sleep)')
plt.plot(x_fit, y_fit, color='orange', linestyle='--', label='Estimated Time (No Sleep)')

# CPUSleep plot
x_fit_CPUSleep = np.linspace(0.01, 10.5, 100)
y_fit_CPUSleep = 1 / (slope_CPUSleep / x_fit_CPUSleep + intercept_CPUSleep)
print(y_fit_CPUSleep)

plt.scatter(intervals, total_minutes, color='blue', label='Data (CPU Sleep)')
ax.plot(x_fit_CPUSleep, y_fit_CPUSleep, color='c', linestyle='--', label='Estimated Time (CPU Sleep)')


ax.set_xlim(0, max(x_fit) )
ax.set_ylim(0, 2150)
ax.set_xlabel('Interval (min)')
ax.set_ylabel('Operation Time (min)')

plt.title("Comparison: CPU Sleep vs No Sleep")
plt.grid(True)
plt.legend(fontsize=15, loc='lower right')
plt.show()