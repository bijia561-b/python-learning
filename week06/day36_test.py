# Day 36 测验：计算每日付费率、找出付费率最高日，并计算 9 月 9 日玩家的次日留存

import pandas as pd
from pathlib import Path

file_path="week06/output/day35_cleaned.csv"
table=pd.read_csv(file_path)
table["login_date"]=pd.to_datetime(table["login_date"]).dt.date
days=sorted(table["login_date"].unique())

# 分别筛选出 8 号、9 号、10 号三天的数据，并计算当天的付费率（当天付费去重人数 ÷ 当天总去重人数）
day8=table[table["login_date"]==days[0]]
pay_rate8=(
    day8[day8["recharge"]>0]["player"].nunique()/day8["player"].nunique()
)
print("8号充值率:",f"{pay_rate8*100:.1f}%")

day9=table[table["login_date"]==days[1]]
pay_rate9=(
    day9[day9["recharge"]>0]["player"].nunique()/day9["player"].nunique()
)
print("9号充值率:",f"{pay_rate9*100:.1f}%")

day10=table[table["login_date"]==days[2]]
pay_rate10=(
    day10[day10["recharge"]>0]["player"].nunique()/day10["player"].nunique()
)
print("10号充值率:",f"{pay_rate10*100:.1f}%")

# 把三天的付费率放进 pd.Series，方便直接用 idxmax() 找出最高的那一天
rates=pd.Series({
    days[0]:pay_rate8,
    days[1]:pay_rate9,
    days[2]:pay_rate10,
})
print("付费率最高的一天:",rates.idxmax())
print("付费率：",f"{rates.max()*100:.1f}%")

# 用集合交集 & 计算 9 号玩家在 10 号的次日留存率
day9_login=set(table[table["login_date"]==days[1]]["player"].unique())
day10_login=set(table[table["login_date"]==days[2]]["player"].unique())
stayed=day9_login&day10_login
print("留存人员:",stayed)
print("9号留存",f"{len(stayed)/len(day9_login)*100:.1f}%")
