# Day 34 测验：生成包含“日期、活跃、收入、新增”的完整活动表并导出为 CSV 和 Excel

import pandas as pd
from pathlib import Path

project_dir=Path(__file__).parent

input_path=project_dir/"day33_login_data.csv"
csv_path=project_dir/"output/day34_test.csv"
excel_path=project_dir/"output/day34_test.xlsx"

table=pd.read_csv(input_path)

table["login_date"]=pd.to_datetime(table["login_date"])

# 使用命名聚合一次性算出每日去重活跃人数和每日充值总收入
data1=table.groupby("login_date").agg(
    活跃=("player","nunique"),
    收入=("recharge","sum")
)
# 找出每个玩家的首次登录日期并统计每日新增人数
data2=table.groupby("player")["login_date"].min()
new_user=data2.value_counts().sort_index()

# 组合成一张新的 DataFrame 复盘表
test_review=pd.DataFrame({"活跃":data1["活跃"],"收入":data1["收入"],"新增":new_user})

# 把日期从索引还原成普通列
test_review=test_review.reset_index()

print(test_review)

# 如果某天没有新增玩家会出现空值，用 fillna(0) 填 0，再用 astype(int) 转为整数
test_review["新增"]=test_review["新增"].fillna(0).astype(int)

# 分别导出为新 CSV 和 Excel 文件，不覆盖原始数据
test_review.to_csv(csv_path,index=False,encoding="utf-8-sig")
print("已导出：",csv_path)
print("原始文件还在",input_path.exists())

test_review.to_excel(excel_path,index=False)
print("已导出：",excel_path)
