# 第 4 周项目（游戏反馈分析工具）：周报生成脚本 report.py——读取分类结果并生成 Markdown 周报

import csv
from pathlib import Path

# 定位当前脚本所在目录及输入、输出文件路径
project_dir=Path(__file__).parent
input_path=project_dir/"output"/"classified_feedback.csv"
report_path=project_dir/"output"/"weekly_report.md"

category_counts={}
total_count=0

# 1. 读取已分类的 CSV 文件，统计总条数与各分类条数
with open (input_path,"r",encoding="utf-8",newline="") as file:
    reader=csv.DictReader(file)

    for row in reader:
        category=row["category"]
        total_count +=1

        if category not in category_counts:
            category_counts[category]=0

        category_counts[category]+=1

# 2. 将统计结果按 Markdown 语法写入 output/weekly_report.md（\n 表示换行）
with open(report_path,"w",encoding="utf-8") as file:
    file.write("#玩家反馈周报\n\n")
    file.write(f"反馈总数：{total_count} 条\n\n")
    file.write("## 分类统计\n\n")

    for category,count in category_counts.items():
        file.write(f"-{category}:{count}条\n")

print ("周报已生成")
