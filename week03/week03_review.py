import csv
import json
from feedback_utils import classify_feedback

input_path="week03/week03_review_feedback.txt"
csv_path="week03/week03_classified_feedback.csv"
json_path="week03/week03_summary.json"

try:
    with open(input_path,"r",encoding="utf-8") as file:
        feedback_lines=file.read().splitlines()
except FileNotFoundError:
    print("找不到反馈文件")
else:
    classified_rows=[]
    category_counts={}
    valid_feedback=[]

    for feedback in feedback_lines:
        category=classify_feedback(feedback)

        row={
            "feedback":feedback,
            "category":category
        }
        classified_rows.append(row)
        if category not in "缺失":
            valid_feedback.append(row)


        if category not in category_counts:
            category_counts[category]=0

        category_counts[category]+=1

    with open(csv_path,"w",encoding="utf-8",newline="") as file:
        fieldnames=["feedback","category"]
        writer=csv.DictWriter(file,fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(classified_rows)
    summary={
        "total_line_count":len(classified_rows),
        "category_counts":category_counts,
        "source_file":input_path,
        "valid_feedback_count":len(valid_feedback)
    }
    with open(json_path,"w",encoding="utf-8")as file:
        json.dump(summary,file,ensure_ascii=False,indent=2)

    print(f"有效反馈：{summary['valid_feedback_count']}")
    print(f"总数：{summary['total_line_count']}")

    for category,count in category_counts.items():
        print(f"{category}:{count}")