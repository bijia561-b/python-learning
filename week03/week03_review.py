# Day 21：第 3 周综合复盘——读取 TXT 反馈、调用分类模块、导出 CSV 明细与 JSON 汇总

import csv
import json
# 从自定义模块 feedback_utils.py 中导入分类函数
from feedback_utils import classify_feedback

input_path="week03/week03_review_feedback.txt"
csv_path="week03/week03_classified_feedback.csv"
json_path="week03/week03_summary.json"

# 1. 安全读取 TXT 文件，捕获文件不存在的异常
try:
    with open(input_path,"r",encoding="utf-8") as file:
        feedback_lines=file.read().splitlines()
except FileNotFoundError:
    print("找不到反馈文件")
else:
    classified_rows=[]
    category_counts={}
    valid_feedback=[]

    # 2. 遍历每一行反馈并调用函数分类
    for feedback in feedback_lines:
        category=classify_feedback(feedback)

        row={
            "feedback":feedback,
            "category":category
        }
        classified_rows.append(row)
        # 如果不是“缺失”，则算作有效反馈
        if category not in "缺失":
            valid_feedback.append(row)

        # 统计各分类数量
        if category not in category_counts:
            category_counts[category]=0

        category_counts[category]+=1

    # 3. 将分类明细写入 CSV 文件
    with open(csv_path,"w",encoding="utf-8",newline="") as file:
        fieldnames=["feedback","category"]
        writer=csv.DictWriter(file,fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(classified_rows)

    # 4. 组装汇总信息并保存为 JSON 文件
    summary={
        "total_line_count":len(classified_rows),
        "category_counts":category_counts,
        "source_file":input_path,
        "valid_feedback_count":len(valid_feedback)
    }
    with open(json_path,"w",encoding="utf-8")as file:
        json.dump(summary,file,ensure_ascii=False,indent=2)

    # 5. 在终端打印统计摘要
    print(f"有效反馈：{summary['valid_feedback_count']}")
    print(f"总数：{summary['total_line_count']}")

    for category,count in category_counts.items():
        print(f"{category}:{count}")
