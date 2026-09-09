import csv
from pathlib import Path

project_dir=Path(__file__).parent
input_path=project_dir/"output"/"classified_feedback.csv"
perfoemance_path=project_dir/"output"/"performance_report.md"

performance_count=0

with open(input_path,"r",encoding="utf-8",newline="")as file:
    reader=csv.DictReader(file)
    for xx in reader:
        if xx["category"]=="性能":
            performance_count +=1
with open(perfoemance_path,"w",encoding="utf-8",newline="")as file:
    file.write("#性能问题报告\n\n")
    file.write(f"性能问题数量：{performance_count}条")

print("性能报告已完成")