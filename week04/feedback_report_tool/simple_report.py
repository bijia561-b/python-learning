# 第 4 周项目：专项报告脚本 simple_report.py——只统计“性能”类问题数量并生成 Markdown 报告

import csv
from pathlib import Path

project_dir=Path(__file__).parent
input_path=project_dir/"output"/"classified_feedback.csv"
perfoemance_path=project_dir/"output"/"performance_report.md"

# 性能问题计数器，初始为 0
performance_count=0

# 读取分类明细 CSV，遇到 category 为“性能”的行就 +1
with open(input_path,"r",encoding="utf-8",newline="")as file:
    reader=csv.DictReader(file)
    for xx in reader:
        if xx["category"]=="性能":
            performance_count +=1

# 把性能问题统计写入 Markdown 报告文件
with open(perfoemance_path,"w",encoding="utf-8",newline="")as file:
    file.write("#性能问题报告\n\n")
    file.write(f"性能问题数量：{performance_count}条")

print("性能报告已完成")
