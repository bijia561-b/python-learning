import csv
from pathlib import Path

project_dir=Path(__file__).parent
input_path=project_dir/"output"/"classified_feedback.csv"
report_path=project_dir/"output"/"weekly_report.md"

category_counts={}
total_count=0

with open (input_path,"r",encoding="utf-8",newline="") as file:
    reader=csv.DictReader(file)

    for row in reader:
        category=row["category"]
        total_count +=1

        if category not in category_counts:
            category_counts[category]=0

        category_counts[category]+=1

with open(report_path,"w",encoding="utf-8") as file:
    file.write("#玩家反馈周报\n\n")
    file.write(f"反馈总数：{total_count} 条\n\n")
    file.write("## 分类统计\n\n")

    for category,count in category_counts.items():
        file.write(f"-{category}:{count}条\n")

print ("周报已生成")