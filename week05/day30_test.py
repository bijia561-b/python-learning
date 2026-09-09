import pandas as pd
from pathlib import Path

project_dir=Path(__file__).parent
input_path=project_dir/"day29_activity_data.csv"

table=pd.read_csv(input_path)

wechat=table[table["channel"]=="微信"]

sort_wechat=wechat.sort_values(
    by="recharge",
    ascending=False
)
print("题目1")
print(f"{sort_wechat[["player","recharge","channel"]]}")

low_recharge=table[table["recharge"]<10]

sort_low_recharge=low_recharge.sort_values(
    by="recharge",
    ascending=True
)

print("题目2")
print(f"{sort_low_recharge[["player","recharge","channel"]].to_string(index=False)}")

mix_table=table[(table["channel"]=="抖音")&(table["recharge"]>20)]

print("题目3")
print(mix_table)

rank=table.sort_values(
    by="recharge",
    ascending=False
)
print("题目4:排行榜")
print(rank)