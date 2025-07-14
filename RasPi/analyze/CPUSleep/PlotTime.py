import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.ticker as ticker
import matplotlib.dates as mdates


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

# 経過時間のリスト
elapsed_time_list = []
# indexを経過時間に変換
for df in df_list:
    df.index = pd.to_datetime(df.index)
    elapsed_s_1SEC = (df.index - df.index[0])
    df.index = pd.to_timedelta(elapsed_s_1SEC, unit='s')
    df.index = df.index.total_seconds() / 60 / 60
    print(df.index[-1])
    elapsed_time_list.append(df.index[-1])
print(elapsed_time_list)

# 時間間隔のリスト
span_list = [10, 60, 120, 600]

# 近似曲線の表示(対数)
x_data = np.array(span_list)
y_data = np.array(elapsed_time_list)

coefficients = np.polyfit(np.log(x_data), y_data, 1)
a = coefficients[0]
b = coefficients[1]

x_fit = np.linspace(min(x_data), max(x_data), 100)
y_fit = a * np.log(x_fit) + b


# 図示する(横軸: 時間間隔, 縦軸: 持続時間)
plt.figure(figsize=(10, 5))

# 散布図
for i in range(len(span_list)):
    plt.scatter(span_list[i], elapsed_time_list[i], label=f'{span_list[i]} sec')

plt.xlabel("Span (sec)")
plt.ylabel("Operation Duration (hour)")
plt.title("Operation Duration of Various Span")
plt.grid(True)
plt.legend(fontsize=15)

# 目盛りを1刻みに
ax = plt.gca()
ax.tick_params(which='minor', direction='in')
ax.tick_params(which='major', length=5, direction='in')

ax.set_xlim(left=0)
ax.set_ylim(bottom=6)

# 近似曲線
plt.plot(x_fit, y_fit, color='black', linestyle='-')

plt.show()
