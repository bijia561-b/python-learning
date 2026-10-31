# Day 33：日期字段处理与按天统计每日活跃（nunique）和每日新增

import pandas as pd
from pathlib import Path

project_dir=Path(__file__).parent
input_path=project_dir/"day33_login_data.csv"

table=pd.read_csv(input_path)
print("原始表格：")
print(table)

# .dtypes 查看每一列的数据类型（刚从 CSV 读入时，日期列通常是 object 即普通文本）
print("转换前类型：")
print(table.dtypes)

# pd.to_datetime() 把文本格式的日期转换成真正的日期类型（datetime64）
table["login_date"]=pd.to_datetime(table["login_date"])
print("转换后类型")
print(table.dtypes)

# .nunique() 统计“不重复的玩家个数”——同一个人同一天登录多次只算 1 人，这就是日活（DAU）
dau=table.groupby("login_date")["player"].nunique()
print("每日活跃人数：")
print(dau)

# .count() 统计的是总行数（如果有人一天登录 2 次会被算成 2）
rows=table.groupby("login_date")["player"].count()
print("每日记录行数：")
print(rows)

# 计算每日新增：先按玩家分组，用 .min() 找出每个玩家第一次登录的日期
first_day=table.groupby("player")["login_date"].min()
print("每个玩家第一次登录：")
print(first_day)

# .value_counts() 统计每一天各有多少人首次登录，再用 .sort_index() 按日期先后排好序
new_users=first_day.value_counts().sort_index()
print("每日新增")
print(new_users)
