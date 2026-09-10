import pandas  as pd
from pathlib import Path

project_dir=Path(__file__).parent
input_path=project_dir /"day31_dirty_activity_data.csv"

table=pd.read_csv(input_path)
print("原始表格")
print(table)

print("原始行数：",len(table))

print("哪里是空值(True表示空)：")
print(table.isna())

print("每列空值个数：")
print(table.isna().sum())

print("哪些行是重复-true")
print(table.duplicated())

cleaned=table.dropna(subset=["recharge"]).copy()
print("充值空值：",len(cleaned))

cleaned["channel"]=cleaned["channel"].fillna("未知")

cleaned=cleaned.drop_duplicates()
print("去重后行数：",len(cleaned))

print("清洗后表格：")
print(cleaned)

print("清洗后空值个数")
print(cleaned.isna().sum())