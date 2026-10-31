# Day 13：用字典统计反馈分类数量（练习 if/elif/else 互斥分类与字典计数）

# 待分类的玩家反馈列表
feebacks=[
    "游戏加载太慢",
    "战斗时出现卡顿",
    "活动奖励不错",
    "希望增加新角色",
    "游戏加载太慢",
]

# 用字典记录每个分类对应的条数，初始都设为 0
category_counts={
    "性能问题":0,
    "活动问题":0,
    "内容建议":0,
}

# 逐条判断反馈属于哪一类，并把对应分类的数字 +1
for feedback in feebacks:
    if "加载" in feedback or "卡顿" in feedback:
        category_counts["性能问题"]=category_counts["性能问题"]+1
    elif "活动" in feedback:
        category_counts["活动问题"]=category_counts["活动问题"]+1
    else:
        category_counts["内容建议"]=category_counts["内容建议"]+1

print("问题统计分类：")

# 遍历字典，打印每个类别的名称和数量
for category,count in category_counts.items():
    print(f"{category}:{count} 条")
