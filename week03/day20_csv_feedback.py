# Day 20：读写 CSV 表格文件与数据清洗（练习 csv.DictReader / DictWriter）

# 导入 Python 内置的 csv 模块，专门用来处理逗号分隔的表格文件
import csv
input_path="week03/day20_feedback.csv"
output_path="week03/day20_feedback_classified.csv"
new_output_path="week03/day20_player_category.csv"

# 用来存清洗并分类后的所有行
classified_rows=[]
# 用来统计每个分类出现了多少次
category_counts={}

# 打开原始 CSV 文件读取，newline="" 是官方推荐写法，避免空行问题
with open(input_path,"r",encoding="utf-8",newline="") as file:
    # DictReader 会把 CSV 的第一行表头当作字典的键（key），后面每一行都读成一个字典
    reader=csv.DictReader(file)
    for row in reader:
        # 取出 feedback 列，如果为空（None）就用 "" 代替，再用 .strip() 去掉首尾多余空格
        feedback=(row.get("feedback")or"").strip()
        # 根据关键词给反馈打上分类标签
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

        # 清洗玩家名称：如果为空则填为“匿名玩家”
        name=(row.get("player")or"").strip()
        if name=="":
            name="匿名玩家"

        # 把清洗后的字段和新增的分类写回当前行字典 row
        row["feedback"]=feedback
        row["category"]=category
        row["player"]=name

        # .get(category, 0) 表示：如果字典里还没有这个分类就取 0，然后 +1
        category_counts[category]=category_counts.get(category,0)+1
        classified_rows.append(row)

# 将包含完整 4 列的分类结果写入新 CSV（"w" 表示写入模式）
with open(output_path,"w",encoding="utf-8",newline="") as file:
    fieldnames=["id","player","feedback","category"]
    writer=csv.DictWriter(file,fieldnames=fieldnames)
    # 写入第一行表头
    writer.writeheader()    
    # 一次性写入所有行
    writer.writerows(classified_rows)

# 再导出一份只含 player 和 category 两列的精简版 CSV
with open(new_output_path,"w",encoding="utf-8",newline="")as file:
    fieldnames=["player","category"]
    writer=csv.DictWriter(file,fieldnames=fieldnames)
    writer.writeheader()

    for row in classified_rows:
        new_row={
            "player":row["player"],
            "category":row["category"]
        }
        # 逐行写入精简字典
        writer.writerow(new_row)

print(f"读取行数：{len(classified_rows)}")

for row in classified_rows:
    print(f"{row['player']}:{row['category']}")
print("分类统计：")
for category,count in category_counts.items():
    print(f"{category}:{count}次")
