feedbacks=[
    "活动奖励不错",
    "游戏加载太慢",
    "希望增加新角色",
    "战斗时出现卡顿",
    "客服回复很及时",
]

performance_feedbacks=[]

for feedback in feedbacks:
    if "加载" in feedback or "卡顿" in feedback:
        performance_feedbacks.append(feedback)

print(f"性能问题数量：{len(performance_feedbacks)}")
for index,feedback in enumerate(performance_feedbacks,start=1):
    print(f"{index}.{feedback}")