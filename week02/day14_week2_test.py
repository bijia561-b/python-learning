# Day 14：第 2 周综合复习——AI 功能运行状态报告（结合字典列表、筛选、汇总字典）

# 5 个 AI 功能的运行数据列表
features = [
    {
        "name": "反馈", "status": "online", "call_count": 120, "error_count": 3,
    },
    {
        "name": "问答", "status": "online", "call_count": 130, "error_count": 0,
    },
    {
        "name": "图片", "status": "online", "call_count": 140, "error_count": 4,
    },
    {
        "name": "音频", "status": "offline", "call_count": 10, "error_count": 0,
    },
    {
        "name": "视频", "status": "offline", "call_count": 20, "error_count": 2,
    },
]

# 用来收集出现过报错（error_count > 0）的功能
error_features = []
# 用来保存整体汇总指标的字典
summary_data = {
    "功能总数": len(features),
    "在线功能数": 0,
    "总调用次数": 0,
    "异常功能数": 0,
}

print("=== AI 功能运行状态报告 ===")

# 遍历每个功能，打印明细并累加统计数据
for feature in features:
    print(
        f"功能名称：{feature['name']}，"
        f"状态：{feature['status']}，"
        f"调用次数：{feature['call_count']}，"
        f"失败次数：{feature['error_count']}"
    )

    # 累加总调用次数
    summary_data["总调用次数"] = (
        summary_data["总调用次数"] + feature["call_count"]
    )

    # 统计在线功能数
    if feature["status"] == "online":
        summary_data["在线功能数"] = summary_data["在线功能数"] + 1

    # 筛选出失败次数大于 0 的异常功能
    if feature["error_count"] > 0:
        error_features.append(feature)

# 异常功能列表的长度就是异常功能数
summary_data["异常功能数"] = len(error_features)

print()
print("=== 汇总数据 ===")

# 打印汇总字典中的每一项指标
for category, count in summary_data.items():
    print(f"{category}：{count}")
print()

# 打印所有异常功能的名单
print(f"异常功能数量：{len(error_features)}")
for index, feature in enumerate(error_features, start=1):
    print(f"{index}.{feature['name']}")
