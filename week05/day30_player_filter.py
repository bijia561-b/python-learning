# Day 30：Pandas 条件筛选与排序（找出高充值玩家并按金额排序）

import pandas as pd
file_path="week05/day29_activity_data.csv"

activity_data=pd.read_csv(file_path)

# 条件筛选：activity_data["recharge"] >= 30 会对每一行判断真假，外层再套 activity_data[...] 就只保留为 True 的行
high_value_players=activity_data[activity_data["recharge"]>=30]

print("充值金额大于30")
# [["player", "recharge"]] 表示只选这两列；.to_string(index=False) 表示打印时不显示左侧行号索引
print(f"{high_value_players[['player','recharge']].to_string(index=False)}")

# .sort_values(by="recharge", ascending=False) 表示按 recharge 列排序，ascending=False 是从高到低（降序）
sort=activity_data.sort_values(
    by="recharge",
    ascending=False
)
# 打印充值最高的前 3 名
print(sort.head(3))
