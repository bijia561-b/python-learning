# Day 8：玩家反馈列表（练习 list 列表、len() 长度、索引 [0]、append() 追加与 for 循环）

# 用方括号 [] 创建一个列表（list），可以按顺序存放多条文本
feedbacks = [
    "活动奖励不错",
    "游戏加载太慢",
    "希望增加新角色",
]

# len(feedbacks) 用于统计列表里一共有多少个元素
print(f"反馈数量：{len(feedbacks)}")

# Python 的索引（位置编号）从 0 开始，所以 feedbacks[0] 取的是第 1 条反馈
print(f"第一条反馈：{feedbacks[0]}")

# .append(...) 会在列表末尾新加一条数据
feedbacks.append("客服回复很及时")

print("全部反馈：")
# for 循环：把列表 feedbacks 里的每一条依次取出来，起名叫 feedback，逐行打印
for feedback in feedbacks:
    print(feedback)
