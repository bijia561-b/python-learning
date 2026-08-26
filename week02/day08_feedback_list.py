feedbacks = [
    "活动奖励不错",
    "游戏加载太慢",
    "希望增加新角色",
]

print(f"反馈数量：{len(feedbacks)}")
print(f"第一条反馈：{feedbacks[0]}")

feedbacks.append("客服回复很及时")

print("全部反馈：")
for feedback in feedbacks:
    print(feedback)
