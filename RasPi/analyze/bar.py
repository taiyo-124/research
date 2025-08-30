import matplotlib.pyplot as plt
import numpy as np

labels = ['Both', 'LoRa', 'No']

# 数値情報[静的電力, 比(D/S)]
NoSleep = [0.0017585170352619449, 0.03373244164977128]
LoRaSleep = [0.0006262920437058747, 0.05507758566403948]
BothSleep = [0.0005021979888173577, 0.10569406111356766]

print("=== 動的電力 ===")
print(f"NoSleep 動的電力:{NoSleep[0] * NoSleep[1]}")
print(f"LoRaSleep 動的電力:{LoRaSleep[0] * LoRaSleep[1]}")
print(f"BothSleep 動的電力:{BothSleep[0] * BothSleep[1]}\n")

# No → LoRa
print("=== No Sleep to LoRa Sleep ===")
print(f"Dybamic Power:{100 *(LoRaSleep[0]*LoRaSleep[1]/(NoSleep[0]*NoSleep[1])-1)}増")
print(f"Static Power:{100 * (1-LoRaSleep[0]/NoSleep[0])}減")
print(f"全体:{100 * (1- (LoRaSleep[0]*(1 + LoRaSleep[1]))/(NoSleep[0]*(1 + NoSleep[1])))}減\n")

# LoRa → Both
print("=== LoRa Sleep to Both Sleep ===")
print(f"Dybamic Power:{100 *(BothSleep[0]*BothSleep[1]/(LoRaSleep[0]*LoRaSleep[1])-1)}増")
print(f"Static Power:{100 * (1-BothSleep[0]/LoRaSleep[0])}減")
print(f"全体:{100 * (1- (BothSleep[0]*(1 + BothSleep[1]))/(LoRaSleep[0]*(1 + LoRaSleep[1])))}減")

# 総計
print("=========================")
print(f"全体:{100 * (1- (BothSleep[0]*(1 + BothSleep[1]))/(NoSleep[0]*(1 + NoSleep[1])))}減")

y_pos = np.arange(3)
# plot
plt.figure(figsize=(4, 4))
ax = plt.gca()

# 棒の高さ
bar_height = 0.3

# 1本目の棒(Both Sleep)
ax.barh(y_pos[0], BothSleep[0]*BothSleep[1] , height=bar_height, color='red')
ax.barh(y_pos[0], BothSleep[0], height=bar_height ,left=BothSleep[0]*BothSleep[1], color='c')

# 2本目の棒(LoRa Sleep)
ax.barh(y_pos[1], LoRaSleep[0]*LoRaSleep[1], height=bar_height, color='red')
ax.barh(y_pos[1], BothSleep[0], height=bar_height ,left=LoRaSleep[0]*LoRaSleep[1], color='c')
ax.barh(y_pos[1], LoRaSleep[0]-BothSleep[0], height=bar_height ,left=LoRaSleep[0]*LoRaSleep[1]+BothSleep[0], color='green')

# 3本目の棒(No Sleep)
ax.barh(y_pos[2], NoSleep[0]*NoSleep[1], height=bar_height, color='red', label='Dynamic')
ax.barh(y_pos[2], BothSleep[0], height=bar_height ,left=LoRaSleep[0]*LoRaSleep[1], color='c', label='Static(1min)')
ax.barh(y_pos[2], LoRaSleep[0]-BothSleep[0], height=bar_height ,left=LoRaSleep[0]*LoRaSleep[1]+BothSleep[0], color='green', label="CPU Idle(1min)")
ax.barh(y_pos[2], NoSleep[0]-(LoRaSleep[0]-BothSleep[0]), height=bar_height ,left=LoRaSleep[0]*LoRaSleep[1]+BothSleep[0]+LoRaSleep[0]-BothSleep[0], color='orange', label='LoRa Idle(1min)')


# 点線プロット
x_1 = NoSleep[0]-(LoRaSleep[0]-BothSleep[0]) + LoRaSleep[0]*LoRaSleep[1]+BothSleep[0]+LoRaSleep[0]-BothSleep[0]
y_1 = y_pos[2] - bar_height/2

x_2 = LoRaSleep[0]-BothSleep[0] + LoRaSleep[0]*LoRaSleep[1]+BothSleep[0]
y_2 = y_pos[1] + bar_height/2

x_3 = LoRaSleep[0]-BothSleep[0] + LoRaSleep[0]*LoRaSleep[1]+BothSleep[0]
y_3 = y_pos[1] - bar_height/2

x_4 = BothSleep[0] + BothSleep[0]*BothSleep[1]
y_4 = y_pos[0] + bar_height/2

ax.plot([x_1, x_2], [y_1, y_2], color='blue', linestyle='--')
ax.plot([x_3, x_4], [y_3, y_4], color='blue', linestyle='--')

# テキスト
ax.text(0.00145, 1.35, "-63.6%", fontsize=10, color='blue')
ax.text(0.00019, 0.45, "-16.0%", fontsize=10, color='blue')

ax.tick_params(axis='y', which='both', length=0)
ax.set_xticks([])
ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=14)
ax.set_ylim(-0.5, len(labels) - 1 + 0.5)

plt.legend(fontsize=12, frameon=True, edgecolor='black')
plt.tight_layout()
plt.show()  