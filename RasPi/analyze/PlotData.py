import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from tkinter import Calendar
import os

# プロット関数
def load_and_plot(selected_date):
    # 日付を 'YYYYMMDD' 形式に変換
    date_str = selected_date.strftime('%Y%m%d')
    file_path = f'/home/kawashima/RawData/{date_str}.csv'

    if not os.path.exists(file_path):
        messagebox.showerror("ファイルエラー", f"ファイルが見つかりません:\n{file_path}")
        return

    df = pd.read_csv(file_path, index_col=0, parse_dates=True)

    # プロット
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df["voltage"], label="Voltage (V)", color="green")
    plt.title(f"Sensor Data on {selected_date.strftime('%Y-%m-%d')}")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

