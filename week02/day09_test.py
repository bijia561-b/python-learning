# Day 9 测验：AI 功能字典（练习字典读取、修改、新增与遍历）

# 定义描述单个 AI 功能的字典
feature={
    "name":"service",
    "call_count":100,
    "success_count":80,
    "per_call_cost":2.01,
}

# 读取并打印字典中的指定字段
print(f"功能名称：{feature['name']}")
print(f"调用次数：{feature['call_count']}")

# 修改已有字段 success_count 的值为 90
feature["success_count"]=90
# 新增字段 status，值为 "online"
feature["status"]="online"

print("更新后的使用信息")
# 遍历打印字典中所有的键值对
for key,value in feature.items():
    print(f"{key}:{value}")
