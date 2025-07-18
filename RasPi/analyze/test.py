# ここに間隔(単位は分)と動作時間(単位は時間)の実測値を入力する
Interval_list = [2, 10]
Time_list = [30.5, 33]

static_power = 60 * (Time_list[0] / Interval_list[0] - Time_list[1] / Interval_list[1]) / (Time_list[1] - Time_list[0]) 
print(f"Static Power = {static_power}")

# 理論上求めたい間隔(分)を入力
Interval = 1 / 6

predict_time = ((60/Interval_list[0] + static_power) * Time_list[0]) / (60/Interval + static_power)
print(f"Time Predicted = {predict_time}")