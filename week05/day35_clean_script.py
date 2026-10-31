# Day 35：第 5 周综合复盘脚本——读取脏数据、清洗、回答 3 个业务问题并导出明细与复盘表
#字段说明
#player：玩家名 str
#channel:渠道；空值填'未知'
#recharge:充值金额；空值删行
#login_date:登录日期；读入后转成日期

import pandas as pd
from pathlib import Path

# 定位输入文件与 output 输出文件夹
project_path=Path(__file__).parent
input_path=project_path/"day35_dirty_activity.csv"
output=project_path/"output"
output.mkdir(exist_ok=True)

clean_path=project_path/"output"

# 1. 读取原始脏数据并把登录日期转成纯日期（.dt.date 去掉具体时分秒）
table=pd.read_csv(input_path)
table["login_date"]=pd.to_datetime(table["login_date"]).dt.date

print("原始行",len(table))
print("空值",table.isna())

# 2. 按业务规则清洗：删掉充值缺失行 -> 渠道缺失填“未知” -> 删除完全重复行
table=table.dropna(subset=["recharge"]).copy()
table["channel"]=table["channel"].fillna("未知")
table=table.drop_duplicates()

print("清洗后",len(table))

# 3. 回答业务问题 1：按渠道求充值总和，找出收入最高的渠道与金额
channel=table.groupby("channel")["recharge"].sum()
print(channel.idxmax(),channel.max())

# 回答业务问题 2：按日期统计去重活跃人数（nunique），找出活跃最多的一天与人数
login_date=table.groupby("login_date")["player"].nunique()
print(login_date.idxmax(),login_date.max())

# 回答业务问题 3：按日期统计充值总和，找出收入最高的一天与金额
day_recharge=table.groupby("login_date")["recharge"].sum()
print(day_recharge.idxmax(),day_recharge.max())

# 计算每日新增：先找每人首次登录日，再统计每天有几人首登
first_login=table.groupby("player")["login_date"].min()
new_user=first_login.value_counts().sort_index()

# 4. 导出清洗后的明细表，并读取前 3 行验证
table.to_csv(output/"day35_cleaned.csv",index=False,encoding="utf-8-sig")
print("清洗明细已导出",(output/"day35_cleaned.csv").exists())
print(pd.read_csv(output/"day35_cleaned.csv").head(3).to_string(index=False))

# 5. 组装并导出按天汇总的复盘表
review=pd.DataFrame({
    "活跃":login_date,
    "新增":new_user,
    "收入":day_recharge
})

review.index.name="日期"
review.to_csv(output/"day35_daily_review.csv",encoding="utf-8-sig")
print("复盘已导出",(output/"day35_daily_review.csv").exists())
print(pd.read_csv(output/"day35_daily_review.csv").head(3).to_string(index=False))
