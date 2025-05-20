import numpy as np
import pandas as pd

# txtファイルを前処理 (MAY19ディレクトリのHOUR?.txtを連結したい)
# ディレクトリ情報: MAY19ディレクトリにHOUR?.txtファイルがある. ?: 0~20


# 各ファイルを読み込んでDataFrame化し, リストに格納
df_list = [pd.read_csv(f'/home/kawashima/Data/RawData/MAY19/HOUR{hour}.TXT', delim_whitespace=True, header=None) for hour in range(0, 21)]

# データを縦方向に連結(列名も設定)
merged_df = pd.concat(df_list, ignore_index=True)
merged_df.columns = ["millis", "temperature", "humidity", "pressure", "voltage"]

# csvファイルで保存
merged_df.to_csv('/home/kawashima/Data/SDCard/1MinSD.csv', index=False)