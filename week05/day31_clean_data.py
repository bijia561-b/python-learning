import pandas  as pd
from pathlib import Path

project_dir=Path(__file__).parent
input_path=project_dir /"day31_dirty_activity_data.csv"

activity_data=pd.read_csv(input_path)

print("原始行数:",len(activity_data))

cleaned_data=activity_data.dropna(subset=["recharge"]).copy()
cleaned_data["channel"]=cleaned_data["channel"].fillna("未知")
cleaned_data=cleaned_data.drop_duplicates()

print("清洗后行数：",len(cleaned_data))
print(cleaned_data)
print(cleaned_data.isna().sum().sum())