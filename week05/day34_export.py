# Day 34：导出复盘数据到 CSV 和 Excel（遵守“读原始文件、写新文件，绝不覆盖原文件”规则）

import pandas as pd
from pathlib import Path

project_dir=Path(__file__).parent
input_path=project_dir/"day33_login_data.csv"

# 准备 output 输出文件夹；mkdir(exist_ok=True) 表示如果文件夹不存在就自动创建，已存在也不报错
output_dir=project_dir/"output"
output_dir.mkdir(exist_ok=True)
output_path=output_dir/"day34_daily_review.csv"

table=pd.read_csv(input_path)
table["login_date"]=pd.to_datetime(table["login_date"])

# 分别计算每日活跃和每日收入
dau=table.groupby("login_date")["player"].nunique()
revenue=table.groupby("login_date")["recharge"].sum()

# 用 pd.DataFrame(...) 把活跃和收入合并成一张新的复盘表
review=pd.DataFrame({"活跃":dau,"收入":revenue})
# .reset_index() 把左侧的日期索引变回普通列，这样导出时才不会丢掉日期列
review=review.reset_index()

print("复盘表：")
print(review)

# .to_csv() 导出为 CSV：index=False 表示不要把 0,1,2 行号写进文件；encoding="utf-8-sig" 防止 Windows Excel 打开中文乱码
review.to_csv(output_path,index=False,encoding="utf-8-sig")
print("已导出：",output_path)
# .exists() 检查原始文件是否完好无损
print("原始文件还在：",input_path.exists())

# .to_excel() 导出为 Excel（.xlsx）文件，底层依赖 openpyxl 库
excel_path=output_dir/"day34_daily_review.xlsx"
review.to_excel(excel_path,index=False)
print("已导出",excel_path)
