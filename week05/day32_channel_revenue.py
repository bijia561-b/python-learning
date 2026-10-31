# Day 32：分组聚合 groupby——按渠道统计总收入、人数、人均，并找出最高收入渠道

import pandas as pd
file_path="week05/day29_activity_data.csv"

table=pd.read_csv(file_path)
print("原始表格")
print(table)

# groupby("channel")["recharge"].sum()：按 channel 列把行分成几组，再对每组的 recharge 列求和
channel_sum=table.groupby("channel")["recharge"].sum()
print("各渠道充值总和：")
print(channel_sum)

# .count() 统计每个渠道组里有多少条记录（即人数）
channel_count=table.groupby("channel")["recharge"].count()
print("各渠道人数：")
print(channel_count)

# 把各渠道收入从高到低排序
ranked=channel_sum.sort_values(ascending=False)
print("收入从高到低：")
print(ranked)

# .idxmax() 返回最大值对应的名称（即哪个渠道最高）；.max() 返回最大的那个数值（即最高金额是多少）
print("收入最高渠道：",channel_sum.idxmax())
print("该渠道收入:",channel_sum.max())

# .agg(["sum", "count", "mean"]) 一次性算出每组的总和（sum）、人数（count）和平均值（mean）
summary=table.groupby("channel")["recharge"].agg(["sum","count","mean"])
print("一张表看总和、人数、人均")
print(summary)
