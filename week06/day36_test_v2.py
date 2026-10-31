# Day 36 测验精简版 v2：用 groupby 直接算出每日付费率，并计算 9 号次日留存

import pandas as pd
from pathlib import Path

project_dir = Path(__file__).parent
table = pd.read_csv(project_dir / "output" / "day35_cleaned.csv")
table["login_date"] = pd.to_datetime(table["login_date"]).dt.date

# 按日期分组求每日 DAU 和每日付费人数，两列直接相除就得到每日付费率
daily_dau = table.groupby("login_date")["player"].nunique()
daily_payers = table[table["recharge"] > 0].groupby("login_date")["player"].nunique()
daily_pay_rate = (daily_payers / daily_dau).fillna(0)

print("每日付费率：")
for day, rate in daily_pay_rate.items():
    print(f"{day}: {rate * 100:.1f}%")
print("付费率最高的一天：", daily_pay_rate.idxmax())
print("付费率：", f"{daily_pay_rate.max() * 100:.1f}%")

# 计算 9 号到 10 号的次日留存
days = sorted(table["login_date"].unique())
day9 = set(table[table["login_date"] == days[1]]["player"])
day10 = set(table[table["login_date"] == days[2]]["player"])
stayed = day9 & day10

print("9号次日还在：", stayed)
print("9号次日留存：", f"{len(stayed) / len(day9) * 100:.1f}%")
