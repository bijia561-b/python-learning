features = [
    {"name": "玩家反馈分类", "status": "online", "call_count": 1200},
    {"name": "智能客服", "status": "offline", "call_count": 400},
    {"name": "运营日报生成", "status": "online", "call_count": 800},
]

online_count = 0

for feature in features:
    print(
        f"功能名称：{feature['name']}，"
        f"状态：{feature['status']}，"
        f"调用次数：{feature['call_count']}"
    )

    if feature["status"] == "online":
        online_count = online_count + 1

print()
print(f"功能总数：{len(features)}")
print(f"在线功能数：{online_count}")
