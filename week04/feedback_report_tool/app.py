import csv
from pathlib import Path

def classified_feedback(feedback):
    if feedback is None or feedback.strip()=="":
        return "缺失"
    elif "卡顿" in feedback:
        return "性能"
    elif "好友" in feedback:
        return "社交"
    elif "登录" in feedback:
        return "登录"
    elif "充值" in feedback:
        return "付费"
    else:
        return "其它"

project_dir=Path(__file__).parent
input_path=project_dir/"data"/"feedback.csv"
output_path=project_dir/"output"/"classified_feedback.csv"

classified_rows=[]

try:
    with open(input_path,"r",encoding="utf-8",newline="") as file:
        reader=csv.DictReader(file)

        for row in reader:
            player=(row.get("player") or "匿名玩家").strip()
            feedback=(row.get("feedback") or "").strip()
            category=classified_feedback(feedback)

            new_row={
                "player":player,
                "feedback":feedback,
                "category":category
            }

            classified_rows.append(new_row)
except FileNotFoundError:
    print("找不到输入文件")

else:
    with open(output_path,"w",encoding="utf-8",newline="")as file:
        fieldnames=["player","feedback","category"]
        writer= csv.DictWriter(file,fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(classified_rows)

    print(f"处理完成:{len(classified_rows)}条反馈")

