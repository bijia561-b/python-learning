#字段说明
#player：玩家名 str
#channel:渠道；空值填'未知'
#recharge:充值金额；空值删行
#login_date:登录日期；读入后转成日期

import pandas as pd
from pathlib import Path

project_path=Path(__file__).parent
input_path=project_path/"day35_dirty_activity.csv"
output=project_path/"output"
output.mkdir(exist_ok=True)

clean_path=project_path/"output"

table=pd.read_csv(input_path)

table["login_date"]=pd.to_datetime(table["login_date"]).dt.date

print("原始行",len(table))

print("空值",table.isna())

table=table.dropna(subset=["recharge"]).copy()

table["channel"]=table["channel"].fillna("未知")

table=table.drop_duplicates()

print("清洗后",len(table))

channel=table.groupby("channel")["recharge"].sum()

print(channel.idxmax(),channel.max())

login_date=table.groupby("login_date")["player"].nunique()

print(login_date.idxmax(),login_date.max())

day_recharge=table.groupby("login_date")["recharge"].sum()

print(day_recharge.idxmax(),day_recharge.max())

first_login=table.groupby("player")["login_date"].min()
new_user=first_login.value_counts().sort_index()

table.to_csv(output/"day35_cleaned.csv",index=False,encoding="utf-8-sig")
print("清洗明细已导出",(output/"day35_cleaned.csv").exists())
print(pd.read_csv(output/"day35_cleaned.csv").head(3).to_string(index=False))

review=pd.DataFrame({
    "活跃":login_date,
    "新增":new_user,
    "收入":day_recharge
})

review.index.name="日期"
review.to_csv(output/"day35_daily_review.csv",encoding="utf-8-sig")
print("复盘已导出",(output/"day35_daily_review.csv").exists())
print(pd.read_csv(output/"day35_daily_review.csv").head(3).to_string(index=False))