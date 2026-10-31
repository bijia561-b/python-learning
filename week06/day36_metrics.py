# Day 36：核心运营指标计算——DAU（日活）、付费率、ARPU（人均收入）、ARPPU（付费用户人均收入）与次日留存

import pandas as pd
from pathlib import Path

project_dir=Path(__file__).parent
table=pd.read_csv(project_dir/"output"/"day35_cleaned.csv")
table["login_date"]=pd.to_datetime(table["login_date"])

# 1. 每日 DAU：按日期分组，统计不重复玩家数（nunique）
dau=table.groupby("login_date")["player"].nunique()
print("每日DAU:")
print(dau)

# 2. 总体用户数、付费人数（至少有一笔 recharge > 0 的去重玩家数）与总收入
users=table["player"].nunique()
payers=table[table["recharge"]>0]["player"].nunique()
revenue=table["recharge"].sum()

# 付费率 = 付费人数 ÷ 总用户数
pay_rate=payers/users
# ARPU = 总收入 ÷ 总用户数（所有活跃用户平均贡献多少钱）
arpu=revenue/users
# ARPPU = 总收入 ÷ 付费人数（只看掏了钱的玩家平均付多少钱）
arppu=revenue /payers

print("用户数：",users)
print("付费人数：",payers)
print("付费率：",f"{pay_rate*100:.1f}%")
print("总收入：",revenue)
# round(数值, 2) 把小数四舍五入保留 2 位
print("arpu:",round(arpu,2))
print("arppu:",round(arppu,2))

# 3. 计算次日留存率：先把不重复的日期按先后排好序
days=sorted(table["login_date"].unique())
print("日期：",days)

# set(...) 把某天登录的玩家转成“集合”（自动去重，并支持用 & 求交集）
day0=set(table[table["login_date"]==days[0]]["player"])
day1=set(table[table["login_date"]==days[1]]["player"])

# day0 & day1 取出既在第 1 天登录、又在第 2 天登录的玩家（即留存下来的玩家）
stayed=day0&day1
# 次日留存率 = 次日还在的人数 ÷ 首日总人数
d1=len(stayed)/len(day0)

print("8号玩家:",day0)
print("9号玩家:",day1)
print("次日还在:",stayed)
print("8号的次日留存:",f"{d1*100:.1f}%")
