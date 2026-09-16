import pandas as pd
from pathlib import Path

project_dir = Path(__file__).parent
input_path = project_dir / "day33_login_data.csv"
output_dir = project_dir / "output"
output_dir.mkdir(exist_ok=True)

csv_path = output_dir / "day34_activity_table.csv"
excel_path = output_dir / "day34_activity_table.xlsx"

table = pd.read_csv(input_path)
table["login_date"] = pd.to_datetime(table["login_date"])

review = table.groupby("login_date").agg(
    活跃=("player", "nunique"),
    收入=("recharge", "sum"),
)

first_day = table.groupby("player")["login_date"].min()
review["新增"] = first_day.value_counts()
review["新增"] = review["新增"].fillna(0).astype(int)

review = review.reset_index()
print(review)

review.to_csv(csv_path, index=False, encoding="utf-8-sig")
review.to_excel(excel_path, index=False)

print("已导出：", csv_path)
print("已导出：", excel_path)
print("原始文件还在：", input_path.exists())
