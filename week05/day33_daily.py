import pandas as pd
from pathlib import Path

project_dir=Path(__file__).parent
input_path=project_dir/"day33_login_data.csv"

table=pd.read_csv(input_path)
print("原始表格：")
print(table)

print("转换前类型：")
print(table.dtypes)

table["login_date"]=pd.to_datetime(table["login_date"])
print("转换后类型")
print(table.dtypes)

dau=table.groupby("login_date")["player"].nunique()
print("每日活跃人数：")
print(dau)

rows=table.groupby("login_date")["player"].count()
print("每日记录行数：")
print(rows)

first_day=table.groupby("player")["login_date"].min()
print("每个玩家第一次登录：")
print(first_day)

new_users=first_day.value_counts().sort_index()
print("每日新增")
print(new_users)