import matplotlib.pyplot as plt
import numpy as np

labels = ['CPU Sleep', 'No Sleep']

# 数値情報[静的電力, 比(D/S)]
NoSleep = [1/1588, 0.0551]
CPUSleep = [1/1971, 0.1057]

print(f"NoSleep 動的電力:{NoSleep[0] * NoSleep[1]}")
print(f"CPUSleep 動的電力:{CPUSleep[0] * CPUSleep[1]}")

print(f"Dybamic Power:{100 *(CPUSleep[0]*CPUSleep[1]/(NoSleep[0]*NoSleep[1])-1)}増")
print(f"Static Power:{100 * (1-CPUSleep[0]/NoSleep[0])}減")
print(f"全体:{100 * (1- (CPUSleep[0]*(1 + CPUSleep[1]))/(NoSleep[0]*(1 + NoSleep[1])))}減")

y_pos = np.arange(2)
print(y_pos)
# plot
plt.figure(figsize=(8, 4))
ax = plt.gca()

# 棒の高さ
bar_height = 0.3

# 点線plot
x_1 = NoSleep[0] * (1 + NoSleep[1])
y_1 = y_pos[1] - bar_height/2

x_2 = CPUSleep[0] * (1 + CPUSleep[1])
y_2 = y_pos[0] + bar_height/2

x_3 = NoSleep[0] * NoSleep[1]
y_3 = y_pos[1] - bar_height/2

x_4 = CPUSleep[0] * CPUSleep[1]
y_4 = y_pos[0] + bar_height/2


# 1本目の棒(No Sleep)
ax.barh(y_pos[1], NoSleep[0]*CPUSleep[1], height=bar_height, color='red', label='Dynamic Power')
ax.barh(y_pos[1], NoSleep[0], height=bar_height ,left=NoSleep[0]*NoSleep[1], color='blue', label='Static Power')

# 2本目の棒(CPU Sleep)
ax.barh(y_pos[0], CPUSleep[0]*CPUSleep[1] , height=bar_height, color='red')
ax.barh(y_pos[0], CPUSleep[0], height=bar_height ,left=CPUSleep[0]*CPUSleep[1], color='blue')

ax.plot([x_1, x_2], [y_1, y_2], color='blue', linestyle='--')
ax.plot([x_3, x_4], [y_3, y_4], color='red', linestyle='--')

ax.text(5.5e-5, 0.4, "+54.6%", fontsize=14, color='red')
ax.text(0.00052, 0.4, "-19.4%", fontsize=14, color='blue')

ax.tick_params(axis='y', which='both', length=0)
ax.set_xticks([])
ax.set_yticks(y_pos)
ax.set_yticklabels(['CPU Sleep', 'No Sleep'])
ax.set_ylim(-0.5, len(labels) - 1 + 0.5)
plt.legend()
plt.show()  