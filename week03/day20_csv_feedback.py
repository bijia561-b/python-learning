import csv
input_path="week03/day20_feedback.csv"
output_path="week03/day20_feedback_classified.csv"
new_output_path="week03/day20_player_category.csv"

classified_rows=[]
category_counts={}

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
        elif "登录" in feedback:
            category="登录问题"
        else:
            category="其它"
        name=(row.get("player")or"").strip()
        if name=="":
            name="匿名玩家"
        row["feedback"]=feedback
        row["category"]=category
        row["player"]=name
        category_counts[category]=category_counts.get(category,0)+1
        classified_rows.append(row)

with open(output_path,"w",encoding="utf-8",newline="") as file:
    fieldnames=["id","player","feedback","category"]
    writer=csv.DictWriter(file,fieldnames=fieldnames)
    writer.writeheader()    
    writer.writerows(classified_rows)
with open(new_output_path,"w",encoding="utf-8",newline="")as file:
    fieldnames=["player","category"]
    writer=csv.DictWriter(file,fieldnames=fieldnames)
    writer.writeheader()

    for row in classified_rows:
        new_row={
            "player":row["player"],
            "category":row["category"]
        }
        writer.writerow(new_row)

print(f"读取行数：{len(classified_rows)}")

for row in classified_rows:
    print(f"{row['player']}:{row['category']}")
print("分类统计：")
for category,count in category_counts.items():
    print(f"{category}:{count}次")