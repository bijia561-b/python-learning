# Day 10 测验：AI 功能状态统计（练习列表中嵌套多个字典 + 计数器累加）

# 列表 features 里存放了 3 个字典，每个字典代表一个 AI 功能
features = [
    {"name": "玩家反馈分类", "status": "online", "call_count": 1200},
    {"name": "智能客服", "status": "offline", "call_count": 400},
    {"name": "运营日报生成", "status": "online", "call_count": 800},
]

# 计数器变量：在循环开始前先设为 0，用来统计在线功能有几个
online_count = 0

# 遍历列表，每次取出的 feature 都是一个字典
for feature in features:
    print(
        f"功能名称：{feature['name']}，"
        f"状态：{feature['status']}，"
        f"调用次数：{feature['call_count']}"
    )

    # 如果当前功能的状态是 "online"，就把计数器加 1
    if feature["status"] == "online":
        online_count = online_count + 1

print()
print(f"功能总数：{len(features)}")
print(f"在线功能数：{online_count}")
