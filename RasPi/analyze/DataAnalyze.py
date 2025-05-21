import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates


"""
以下に, データ分析の詳細

電圧値とRSSIのグラフ

"""


# データ読み込み(~/Data/以下指定)
file = 'LoRa/1MINLoRa.csv'
df_LoRa = pd.read_csv(f'/home/kawashima/Data/{file}', index_col=0, skiprows=1, names=["temperature", "humidity", "pressure", "voltage", "RSSI"])


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

# 経過時間に変換(Timedelta型)
df_LoRa.index = pd.to_datetime(df_LoRa.index)
elapsed_s_LoRa = (df_LoRa.index - df_LoRa.index[0])
df_LoRa.index = pd.to_timedelta(elapsed_s_LoRa, unit='s')
# Timedelta型を時間単位に
df_LoRa.index = df_LoRa.index.total_seconds() / 60 / 60 
print(df_LoRa)



# """ 以下, Arduino側でデータを取得したときに実行(df.index: millis()) """

# # df.indexを経過時間(単位:s)に変換
# elapsed_s_SD = (df_SD.index - df_SD.index[0]) / 1000
# df_SD.index = pd.to_timedelta(elapsed_s_SD, unit='s')
# # Timedelta型を時間単位に
# df_SD.index = df_SD.index.total_seconds() / 60 / 60 
# print(df_SD)


""" 以下, 行いたい操作を記述 """

# 経過時間と電圧のグラフを表示

fig, ax1 = plt.subplots()

ax1.scatter(df_LoRa.index, df_LoRa['voltage'], s=5, color='blue', label="Voltage")
ax1.set_xlabel('Elapsed Time [hour]')
ax1.set_ylabel('Voltage [mV]', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
fig.legend(fontsize=15)

ax2 = ax1.twinx()
ax2.scatter(df_LoRa.index, df_LoRa['RSSI'], s=5, color='red', label="RSSI")
ax2.set_ylabel('RSSI [dBm]', color='red')
ax2.tick_params(axis='y', labelcolor='red')

plt.axvline(x=9.369444, color='green', linestyle='--', linewidth=1)
ax1.text(9.75, 3750, "Time: about 9h22m", color='green')

plt.title("Voltage and RSSI Variation")
ax1.grid(True)
fig.legend(fontsize=15)

# 目盛りを1刻みに
ax1.tick_params(which='minor', direction='in')
ax1.tick_params(which='major', length=5, direction='in')
ax1.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax1.xaxis.set_minor_locator(ticker.AutoMinorLocator())
ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax2.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax1.set_xlim(left=0, right=16.5)
ax1.set_ylim(bottom=3350, top=4250)
ax2.set_ylim(bottom=-105, top=-15)
fig.tight_layout()
plt.show()