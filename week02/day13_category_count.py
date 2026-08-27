feebacks=[
    "游戏加载太慢",
    "战斗时出现卡顿",
    "活动奖励不错",
    "希望增加新角色",
    "游戏加载太慢",
]

category_counts={
    "性能问题":0,
    "活动问题":0,
    "内容建议":0,
}

for feedback in feebacks:
    if "加载" in feedback or "卡顿" in feedback:
        category_counts["性能问题"]=category_counts["性能问题"]+1
    elif "活动" in feedback:
        category_counts["活动问题"]=category_counts["活动问题"]+1
    else:
        category_counts["内容建议"]=category_counts["内容建议"]+1

print("问题统计分类：")

for category,count in category_counts.items():
    print(f"{category}:{count} 条")
