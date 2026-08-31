import csv
input_path="week03/day20_feedback.csv"
output_path="week03/day20_feedback_classified.csv"

classified_rows=[]

with open(input_path,"r",encoding="utf-8",newline="") as file:
    reader=csv.DictReader(file)
    for row in reader:
        feedback=(row.get("feedback")or"").strip()
        if feedback=="":
            category="缺失"
        elif"卡顿" in feedback:
            category="性能"
        elif "好友" in feedback:
            category="社交"
        else:
            category="其它"
        row["feedback"]=feedback
        row["category"]=category
        classified_rows.append(row)

with open(output_path,"w",encoding="utf-8",newline="") as file:
    fieldnames=["id","player","feedback","category"]
    writer=csv.DictWriter(file,fieldnames=fieldnames)
    writer.writeheader()    
    writer.writerows(classified_rows)

print(f"读取行数：{len(classified_rows)}")

for row in classified_rows:
    print(f"{row['player']}:{row['category']}")