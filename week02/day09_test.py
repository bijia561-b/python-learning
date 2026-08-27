feature={
    "name":"service",
    "call_count":100,
    "success_count":80,
    "per_call_cost":2.01,
}

print(f"功能名称：{feature['name']}")
print(f"调用次数：{feature['call_count']}")

feature["success_count"]=90
feature["status"]="online"

print("更新后的使用信息")
for key,value in feature.items():
    print(f"{key}:{value}")