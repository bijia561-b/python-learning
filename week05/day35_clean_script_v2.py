# 字段说明
# player：玩家名
# channel：渠道；空值填「未知」
# recharge：充值金额；空值删行
# login_date：登录日期；读入后转成日期

import pandas as pd
from pathlib import Path

project_dir = Path(__file__).parent
input_path = project_dir / "day35_dirty_activity.csv"
output_dir = project_dir / "output"
output_dir.mkdir(exist_ok=True)

cleaned_path = output_dir / "day35_cleaned_v2.csv"
review_path = output_dir / "day35_daily_review_v2.csv"

raw = pd.read_csv(input_path)
print("清洗前行数:", len(raw))
print("每列空值个数:")
print(raw.isna().sum())

table = raw.copy()
table["login_date"] = pd.to_datetime(table["login_date"]).dt.date
table = table.dropna(subset=["recharge"]).copy()
table["channel"] = table["channel"].fillna("未知")
table = table.drop_duplicates()
print("清洗后行数:", len(table))

channel_revenue = table.groupby("channel")["recharge"].sum()
print("收入最高渠道:", channel_revenue.idxmax(), channel_revenue.max())

daily = table.groupby("login_date").agg(
    活跃=("player", "nunique"),
    收入=("recharge", "sum"),
)
first_day = table.groupby("player")["login_date"].min()
daily["新增"] = first_day.value_counts()
daily["新增"] = daily["新增"].fillna(0).astype(int)
daily = daily[["活跃", "新增", "收入"]]
daily.index.name = "日期"

print("活跃最多的一天:", daily["活跃"].idxmax(), daily["活跃"].max())
print("收入最高的一天:", daily["收入"].idxmax(), daily["收入"].max())

table.to_csv(cleaned_path, index=False, encoding="utf-8-sig")
daily.to_csv(review_path, encoding="utf-8-sig")
print("清洗明细已导出:", cleaned_path.exists())
print("复盘已导出:", review_path.exists())
print(pd.read_csv(cleaned_path).head(3).to_string(index=False))
print(pd.read_csv(review_path).head(3).to_string(index=False))
