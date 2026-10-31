# Day 31：数据清洗——检查缺失值与重复值、删除空行（dropna）、填充默认值（fillna）与去重（drop_duplicates）

import pandas  as pd
from pathlib import Path

project_dir=Path(__file__).parent
input_path=project_dir /"day31_dirty_activity_data.csv"

table=pd.read_csv(input_path)
print("原始表格")
print(table)

# len(table) 统计表格当前有多少行
print("原始行数：",len(table))

# .isna() 会把每个格子变成 True（是空值 NaN）或 False（不是空值）
print("哪里是空值(True表示空)：")
print(table.isna())

# .isna().sum() 统计每一列各有几个空值
print("每列空值个数：")
print(table.isna().sum())

# .duplicated() 检查哪些行和前面的行完全重复（重复出现的那行显示 True）
print("哪些行是重复-true")
print(table.duplicated())

# 清洗第 1 步：dropna(subset=["recharge"]) 只删除 recharge 列为空的行；.copy() 复制成独立新表，防止后续修改报警
cleaned=table.dropna(subset=["recharge"]).copy()
print("充值空值：",len(cleaned))

# 清洗第 2 步：fillna("未知") 把 channel 列里的空值填成“未知”
cleaned["channel"]=cleaned["channel"].fillna("未知")

# 清洗第 3 步：drop_duplicates() 删除完全重复的行（只保留第一次出现的那条）
cleaned=cleaned.drop_duplicates()
print("去重后行数：",len(cleaned))

print("清洗后表格：")
print(cleaned)

# 再次检查清洗后是否还有空值（全部为 0 说明空值已处理干净）
print("清洗后空值个数")
print(cleaned.isna().sum())
