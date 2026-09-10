import pandas as pd
filepath="week05/day31_dirty_activity_data.csv"

table=pd.read_csv(filepath)
print("清洗前行数：",len(table))
table["recharge"]=table["recharge"].fillna(0)

table["channel"]=table["channel"].fillna("未知")

table=table.drop_duplicates()
print("清洗后行数：",len(table))
print("清洗后表")
print(table)

print("充值总和:",table["recharge"].sum())

print(table.isna().sum())