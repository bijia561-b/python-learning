import pandas as pd
from pathlib import Path

project_dir=Path(__file__).parent

input_path=project_dir/"day33_login_data.csv"
csv_path=project_dir/"output/day34_test.csv"
excel_path=project_dir/"output/day34_test.xlsx"

table=pd.read_csv(input_path)

table["login_date"]=pd.to_datetime(table["login_date"])

data1=table.groupby("login_date").agg(
    活跃=("player","nunique"),
    收入=("recharge","sum")
)
data2=table.groupby("player")["login_date"].min()

new_user=data2.value_counts().sort_index()

test_review=pd.DataFrame({"活跃":data1["活跃"],"收入":data1["收入"],"新增":new_user})

test_review=test_review.reset_index()

print(test_review)

test_review["新增"]=test_review["新增"].fillna(0).astype(int)

test_review.to_csv(csv_path,index=False,encoding="utf-8-sig")
print("已导出：",csv_path)
print("原始文件还在",input_path.exists())

test_review.to_excel(excel_path,index=False)
print("已导出：",excel_path)