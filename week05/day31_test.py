# Day 31 测验：换用“充值缺失填 0、不删行”的业务规则清洗同一份脏数据

import pandas as pd
filepath="week05/day31_dirty_activity_data.csv"

table=pd.read_csv(filepath)
print("清洗前行数：",len(table))

# 规则 1：充值缺失不删行，而是用 fillna(0) 填成 0 元
table["recharge"]=table["recharge"].fillna(0)

# 规则 2：渠道缺失填成“未知”
table["channel"]=table["channel"].fillna("未知")

# 规则 3：去掉完全重复的行
table=table.drop_duplicates()
print("清洗后行数：",len(table))
print("清洗后表")
print(table)

# .sum() 把 recharge 这一列的所有数字加起来，算出充值总和
print("充值总和:",table["recharge"].sum())

# 检查每列剩余空值数量
print(table.isna().sum())
