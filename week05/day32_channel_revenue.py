import pandas as pd
file_path="week05/day29_activity_data.csv"

table=pd.read_csv(file_path)
print("原始表格")
print(table)

channel_sum=table.groupby("channel")["recharge"].sum()
print("各渠道充值总和：")
print(channel_sum)

channel_count=table.groupby("channel")["recharge"].count()
print("各渠道人数：")
print(channel_count)

ranked=channel_sum.sort_values(ascending=False)
print("收入从高到低：")
print(ranked)

print("收入最高渠道：",channel_sum.idxmax())
print("该渠道收入:",channel_sum.max())

summary=table.groupby("channel")["recharge"].agg(["sum","count","mean"])
print("一张表看总和、人数、人均")
print(summary)