# Day 29：Pandas 入门——认识整张表 DataFrame 与单列 Series

# 导入 pandas 库，并按行业惯例简写为 pd
import pandas as pd
file_path="week05/day29_activity_data.csv"

# pd.read_csv() 把 CSV 文件读成一张 Pandas 表格（叫做 DataFrame）
activity_data=pd.read_csv(file_path)
print("完整表格：")
print(activity_data)

# .head(3) 只查看表格的前 3 行，适合大表快速预览
print("前3行:")
print(activity_data.head(3))

# 用 表格名["列名"] 单独取出一列（单列在 Pandas 中叫做 Series）
recharge_column=activity_data["recharge"]

print("充值列：")
print(recharge_column)

# 单独取出 player（玩家名称）这一列
xx=activity_data["player"]

print("玩家")
print(xx)
