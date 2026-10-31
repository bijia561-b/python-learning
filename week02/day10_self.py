# Day 10 自主练习：统计在线 AI 功能数与总调用次数

# 准备 3 个 AI 功能的字典列表
features=[
    {"name":"ask","status":"online","call_count":80},
    {"name":"image","status":"online","call_count":70},
    {"name":"video","status":"offline","call_count":0},
]
# 初始化两个累加器：在线功能数、总调用次数都从 0 开始
online_features=0
total_call_count=0

for feature in features:
    print(
        f"名称：{feature['name']},"
        f"状态：{feature['status']},"
        f"调用次数:{feature['call_count']:.1f}"
        )
    # 判断是否在线，在线则计数 +1
    if feature["status"]=="online":
        online_features=online_features+1
    # 累加每个功能的调用次数
    total_call_count=total_call_count+feature["call_count"]
print(f"功能总数：{len(features)}")
print(f"在线功能数：{online_features}")
print(f"总调用次数：{total_call_count}次")
