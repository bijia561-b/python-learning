# Day 34 测验标准参考版：汇总每日活跃、收入、新增并安全导出到 CSV 与 Excel

import pandas as pd
from pathlib import Path

# 定位目录并确保 output 文件夹存在
project_dir = Path(__file__).parent
input_path = project_dir / "day33_login_data.csv"
output_dir = project_dir / "output"
output_dir.mkdir(exist_ok=True)

csv_path = output_dir / "day34_activity_table.csv"
excel_path = output_dir / "day34_activity_table.xlsx"

# 读取并转换日期列
table = pd.read_csv(input_path)
table["login_date"] = pd.to_datetime(table["login_date"])

# 按日期分组聚合出活跃（去重人数）与收入（充值求和）
review = table.groupby("login_date").agg(
    活跃=("player", "nunique"),
    收入=("recharge", "sum"),
)

# 计算每个玩家首登日期，按天统计新增人数并补齐空值为整数 0
first_day = table.groupby("player")["login_date"].min()
review["新增"] = first_day.value_counts()
review["新增"] = review["新增"].fillna(0).astype(int)

# 将日期索引还原为普通列后打印
review = review.reset_index()
print(review)

# 导出 CSV 和 Excel
review.to_csv(csv_path, index=False, encoding="utf-8-sig")
review.to_excel(excel_path, index=False)

print("已导出：", csv_path)
print("已导出：", excel_path)
print("原始文件还在：", input_path.exists())
