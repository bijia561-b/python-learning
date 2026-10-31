# Day 32 测验：先筛掉 0 充值玩家，再按渠道统计总收入与人均最高渠道

import pandas as pd
file_path="week05/day29_activity_data.csv"

table=pd.read_csv(file_path)

# != 表示“不等于”：先筛选出充值金额不等于 0 的付费玩家
table1=table[table["recharge"] != 0]

# 按渠道分组求充值总和
table2=table1.groupby("channel")["recharge"].sum()

# 用 idxmax() 取最高渠道名，用 max() 取最高金额
print("收入最高的渠道是：",table2.idxmax(),"，","共",table2.max())

# 按渠道分组求平均充值（mean），并找出人均最高的渠道
table3=table1.groupby("channel")["recharge"].mean()
print("人均最高的渠道：",table3.idxmax())
