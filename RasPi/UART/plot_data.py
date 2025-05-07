import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
import os

Datafile = os.path.expanduser("~/Data/DataPath/log.txt")

# データ用のリスト
timestamps = []
co2_values= []

def read_log_files(Datafile):
    ts, co2s = [], []
    try:
        with open(Datafile, "r") as f:
            for line in f:
                try:
                    timestamp_str, co2_str = line.strip().split(": ")
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    co2 = int(co2_str.replace("ppm", "").strip())
                    ts.append(timestamp)
                    co2s.append(co2)
                except:
                    continue
    except FileNotFoundError:
        pass
    return ts, co2s

def update(frame):
    global timestamps, co2_values

    new_timestamps, new_co2_values = read_log_files(Datafile)
    if new_timestamps:
        timestamps = new_timestamps
        co2_values = new_co2_values

        ax.clear()
        ax.plot(timestamps, co2_values, marker='o', linestyle='-')
        ax.set_xlabel("Time")
        ax.set_ylabel("CO₂ Concentration (ppm)")
        ax.set_title("Real-Time CO₂ Monitoring")
        ax.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()


fig, ax = plt.subplots(figsize=(10, 5))
ani = FuncAnimation(fig, update, interval=5000)  # 5秒ごとに更新
plt.show()