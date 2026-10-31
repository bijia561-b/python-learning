# 第 4 周项目（游戏反馈分析工具）：主处理脚本 app.py——读取原始反馈 CSV、分类并导出明细 CSV

import csv
# Path 用于跨平台拼接文件路径，不管在哪个目录下运行都能准确找到同级文件夹
from pathlib import Path

# 定义反馈分类函数：根据关键词返回对应的问题类别
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

# Path(__file__).parent 表示当前这个 .py 文件所在的文件夹路径
project_dir=Path(__file__).parent
input_path=project_dir/"data"/"feedback.csv"
output_path=project_dir/"output"/"classified_feedback.csv"

classified_rows=[]

# 读取 data/feedback.csv 并逐行分类
try:
    with open(input_path,"r",encoding="utf-8",newline="") as file:
        reader=csv.DictReader(file)

        for row in reader:
            # 若玩家名为空则默认填为“匿名玩家”，并去掉首尾空格
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
    # 将分类后的明细写入 output/classified_feedback.csv
    with open(output_path,"w",encoding="utf-8",newline="")as file:
        fieldnames=["player","feedback","category"]
        writer= csv.DictWriter(file,fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(classified_rows)

    print(f"处理完成:{len(classified_rows)}条反馈")
