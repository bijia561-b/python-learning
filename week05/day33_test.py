# Day 33 测验：按日期统计每日收入（GMV）与活跃人数（DAU），找出收入最高日及当天日活

import pandas as pd
file_path="week05/day33_login_data.csv"

table=pd.read_csv(file_path)

# 将登录日期列转换为日期类型
table["login_date"]=pd.to_datetime(table["login_date"])

# 按日期分组：分别求每日充值总和（gmv）与每日去重活跃人数（dau）
gmv=table.groupby("login_date")["recharge"].sum()
dau=table.groupby("login_date")["player"].nunique()

print(gmv)
print(dau)
# 找出收入最高的那一天日期
best_day=gmv.idxmax()

print(f"收入最高的一天：{gmv.idxmax()},收入为{gmv.max()}")
# 用 dau[best_day] 取出收入最高那一天的活跃人数
print("活跃人数为：",dau[best_day])
