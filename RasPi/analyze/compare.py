import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib.patches as patches
import matplotlib.ticker as ticker
import matplotlib.dates as mdates

""" No Sleep """
# 1. データ前処理
df_NoSleep_list = []

file_NoSleep_10SEC = 'NoSleep/10SEC.csv'
df_NoSleep_10SEC = pd.read_csv(f'/home/kawashima/Data/{file_NoSleep_10SEC}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
df_NoSleep_list.append(df_NoSleep_10SEC)

file_NoSleep_30SEC = 'NoSleep/30SEC.csv'
df_NoSleep_30SEC = pd.read_csv(f'/home/kawashima/Data/{file_NoSleep_30SEC}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
df_NoSleep_list.append(df_NoSleep_30SEC)

file_NoSleep_1MIN = 'NoSleep/1MIN.csv'
df_NoSleep_1MIN = pd.read_csv(f'/home/kawashima/Data/{file_NoSleep_1MIN}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
df_NoSleep_list.append(df_NoSleep_1MIN)

time_list = []

# indexを経過時間(min)に変換
for df in df_NoSleep_list:
    df.index = pd.to_datetime(df.index)
    elapsed_s_1SEC = (df.index - df.index[0])
    df.index = pd.to_timedelta(elapsed_s_1SEC, unit='s')
    df.index = df.index.total_seconds() / 60 
    time_list.append(df.index[-1])

# 時間間隔のリスト 
span_list_NoSleep = np.array([10, 30, 60])
span_list_NoSleep= span_list_NoSleep / 60
print(span_list_NoSleep)

x_NoSleep = 1 / span_list_NoSleep
time_list = np.array(time_list)
y_NoSleep = 1 / time_list

# --- 3. Model Fitting (using numpy.polyfit) ---

# np.polyfit(x_NoSleep, y_NoSleep, 1) returns coefficients [slope_NoSleep, intercept_NoSleep]
slope_NoSleep, intercept_NoSleep = np.polyfit(x_NoSleep, y_NoSleep, 1)
ratio_val = slope_NoSleep / intercept_NoSleep
power_ratio= 1 / (1 / ratio_val)
print("===== No Sleep =====")
print(f"動的電力: {slope_NoSleep}, 静的電力: {intercept_NoSleep}, 比={slope_NoSleep/intercept_NoSleep}\n")


""" LoRa Sleep """
# 1. データ前処理

df_list = []


file_2SEC = 'LoRa/2SEC.csv'
df_2SEC = pd.read_csv(f'/home/kawashima/Data/{file_2SEC}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
df_list.append(df_2SEC)

file_5SEC = 'LoRa/5SEC.csv'
df_5SEC = pd.read_csv(f'/home/kawashima/Data/{file_5SEC}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
df_list.append(df_5SEC)

file_10SEC = 'LoRa/10SEC.csv'
df_10SEC = pd.read_csv(f'/home/kawashima/Data/{file_10SEC}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
df_list.append(df_10SEC)


file_30SEC = 'LoRa/30SEC.csv'
df_30SEC = pd.read_csv(f'/home/kawashima/Data/{file_30SEC}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])
df_list.append(df_30SEC)

file_1MIN = 'LoRa/1MIN.csv'
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
    elapsed_time_list.append(df.index[-1])

# 時間間隔のリスト 
span_list_LoRaSleep = np.array([2, 5, 10, 30, 60])
span_list_LoRaSleep = span_list_LoRaSleep / 60
print(span_list_LoRaSleep)

x_LoRaSleep = 1 / span_list_LoRaSleep
elapsed_time_list = np.array(elapsed_time_list)
y_LoRaSleep = 1 / elapsed_time_list

# --- 3. Model Fitting (using numpy.polyfit) ---

# np.polyfit(x_LoRaSleep, y_LoRaSleep, 1) returns coefficients [slope_LoRaSleep, intercept_LoRaSleep]
slope_LoRaSleep, intercept_LoRaSleep = np.polyfit(x_LoRaSleep, y_LoRaSleep, 1)
ratio_val = slope_LoRaSleep / intercept_LoRaSleep
power_ratio= 1 / (1 / ratio_val)
print("===== LoRa Sleep =====")
print(f"動的電力: {slope_LoRaSleep}, 静的電力: {intercept_LoRaSleep}, 比={slope_LoRaSleep/intercept_LoRaSleep}\n")


""" Both Sleep """
# --- 1. Data Preparation ---
# Interval (minutes)
intervals = np.array([1/6, 1, 2, 10])
# Operating Time (hours, minutes)
durations_h = np.array([20, 30, 30, 33])
durations_m = np.array([19, 8, 57, 19])

# Convert all time units to minutes
total_minutes = durations_h * 60 + durations_m

# --- 2. Data Transformation for Linear Regression ---
# y_BothSleep = 1 / Operating Time
# x_BothSleep = 1 / Interval
x_BothSleep = 1 / intervals
y_BothSleep = 1 / total_minutes

# --- 3. Model Fitting (using numpy.polyfit) ---

# np.polyfit(x_BothSleep, y_BothSleep, 1) returns coefficients [slope, intercept]
slope_BothSleep, intercept_BothSleep = np.polyfit(x_BothSleep, y_BothSleep, 1)


# Case 2: Excluding the suspicious outlier (the last data point)
slope_BothSleep, intercept_BothSleep = np.polyfit(x_BothSleep, y_BothSleep, 1)
ratio_val = slope_BothSleep / intercept_BothSleep
power_ratio= 1 / (1 / ratio_val)
print("===== Both Sleep =====")
print(f"動的電力: {slope_BothSleep}, 静的電力: {intercept_BothSleep}, 比={slope_BothSleep/intercept_BothSleep}\n")


"""" plot """

plt.figure(figsize=(12, 6))

ax = plt.gca()
ax.tick_params(which='minor', direction='in')
ax.tick_params(which='major', length=5, direction='in')
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())

# No Sleep plot
x_fit_NoSleep = np.linspace(0.01, 10.5, 100)
y_fit_NoSleep = 1 / (slope_NoSleep / x_fit_NoSleep + intercept_NoSleep)
plt.scatter(span_list_NoSleep, time_list, color='magenta', label='Data (No Sleep)')
plt.plot(x_fit_NoSleep, y_fit_NoSleep, color='purple', linestyle='--', label='Estimated Time (No Sleep)')

# LoRa Sleep plot
x_fit_LoRaSleep = np.linspace(0.01, 10.5, 100)
y_fit_LoRaSleep = 1 / (slope_LoRaSleep / x_fit_LoRaSleep + intercept_LoRaSleep)
plt.scatter(span_list_LoRaSleep, elapsed_time_list, color='red', label='Data (LoRa Sleep)')
plt.plot(x_fit_LoRaSleep, y_fit_LoRaSleep, color='orange', linestyle='--', label='Estimated Time (LoRa Sleep)')

# Both Sleep plot
x_fit_BothSleep = np.linspace(0.01, 10.5, 100)
y_fit_BothSleep = 1 / (slope_BothSleep / x_fit_BothSleep + intercept_BothSleep)

plt.scatter(intervals, total_minutes, color='blue', label='Data (Both Sleep)')
ax.plot(x_fit_BothSleep, y_fit_BothSleep, color='c', linestyle='--', label='Estimated Time (Both Sleep)')


ax.set_xlim(0, 10.5)
ax.set_ylim(0, 2150)
ax.set_xlabel('Interval (min)', fontsize=16)
ax.set_ylabel('Operation Time (min)', fontsize=16)

plt.title("Comparison: 3 pattern (No Sleep vs LoRa Sleep vs Both Sleep)", fontsize=18)
plt.grid(True)
plt.legend(fontsize=15, loc='center right')
plt.show()