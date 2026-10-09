import pandas as pd
from pathlib import Path

project_dir=Path(__file__).parent
table=pd.read_csv(project_dir/"output"/"day35_cleaned.csv")
table["login_date"]=pd.to_datetime(table["login_date"])

dau=table.groupby("login_date")["player"].nunique()
print("每日DAU:")
print(dau)

users=table["player"].nunique()
payers=table[table["recharge"]>0]["player"].nunique()
revenue=table["recharge"].sum()

pay_rate=payers/users
arpu=revenue/users
arppu=revenue /payers

print("用户数：",users)
print("付费人数：",payers)
print("付费率：",f"{pay_rate*100:.1f}%")
print("总收入：",revenue)
print("arpu:",round(arpu,2))
print("arppu:",round(arppu,2))

days=sorted(table["login_date"].unique())
print("日期：",days)

day0=set(table[table["login_date"]==days[0]]["player"])
day1=set(table[table["login_date"]==days[1]]["player"])

stayed=day0&day1
d1=len(stayed)/len(day0)

print("8号玩家:",day0)
print("9号玩家:",day1)
print("次日还在:",stayed)
print("8号的次日留存:",f"{d1*100:.1f}%")