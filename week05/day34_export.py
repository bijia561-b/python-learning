import pandas as pd
from pathlib import Path

project_dir=Path(__file__).parent
input_path=project_dir/"day33_login_data.csv"

output_dir=project_dir/"output"
output_dir.mkdir(exist_ok=True)
output_path=output_dir/"day34_daily_review.csv"

table=pd.read_csv(input_path)
table["login_date"]=pd.to_datetime(table["login_date"])

dau=table.groupby("login_date")["player"].nunique()

revenue=table.groupby("login_date")["recharge"].sum()

review=pd.DataFrame({"活跃":dau,"收入":revenue})
review=review.reset_index()

print("复盘表：")
print(review)

review.to_csv(output_path,index=False,encoding="utf-8-sig")
print("已导出：",output_path)
print("原始文件还在：",input_path.exists())

excel_path=output_dir/"day34_daily_review.xlsx"
review.to_excel(excel_path,index=False)
print("已导出",excel_path)