# Day 12：筛选性能问题反馈（练习关键字 in 包含判断与列表筛选）

# 原始反馈列表
feedbacks=[
    "活动奖励不错",
    "游戏加载太慢",
    "希望增加新角色",
    "战斗时出现卡顿",
    "客服回复很及时",
]

# 准备一个空列表，专门存放筛选出来的性能问题
performance_feedbacks=[]

for feedback in feedbacks:
    # "加载" in feedback 会判断“加载”这两个字是否出现在当前反馈文本里（返回 True 或 False）
    if "加载" in feedback or "卡顿" in feedback:
        performance_feedbacks.append(feedback)

print(f"性能问题数量：{len(performance_feedbacks)}")
# 打印筛选后的结果
for index,feedback in enumerate(performance_feedbacks,start=1):
    print(f"{index}.{feedback}")
