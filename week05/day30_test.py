# Day 30 测验：单条件筛选、多条件组合筛选（&）与升/降序排列

import pandas as pd
from pathlib import Path

# 定位同目录下的 CSV 数据文件
project_dir=Path(__file__).parent
input_path=project_dir/"day29_activity_data.csv"

table=pd.read_csv(input_path)

# 题目 1：筛选渠道为“微信”的玩家，并按充值金额从高到低排序
wechat=table[table["channel"]=="微信"]

sort_wechat=wechat.sort_values(
    by="recharge",
    ascending=False
)
print("题目1")
print(f"{sort_wechat[['player','recharge','channel']]}")

# 题目 2：筛选充值小于 10 元的玩家，并按充值金额从低到高（ascending=True）排序
low_recharge=table[table["recharge"]<10]

sort_low_recharge=low_recharge.sort_values(
    by="recharge",
    ascending=True
)

print("题目2")
print(f"{sort_low_recharge[['player','recharge','channel']].to_string(index=False)}")

# 题目 3：多条件组合筛选——Pandas 中用 & 表示“并且”，每个条件必须用小括号 () 括起来
mix_table=table[(table["channel"]=="抖音")&(table["recharge"]>20)]

print("题目3")
print(mix_table)

# 题目 4：整张表按充值从高到低排出排行榜
rank=table.sort_values(
    by="recharge",
    ascending=False
)
print("题目4:排行榜")
print(rank)
