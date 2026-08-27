features=[
    {"name":"ask","status":"online","call_count":80},
    {"name":"image","status":"online","call_count":70},
    {"name":"video","status":"offline","call_count":0},
]
online_features=0
total_call_count=0

for feature in features:
    print(
        f"名称：{feature['name']},"
        f"状态：{feature['status']},"
        f"调用次数:{feature['call_count']:.1f}"
        )
    if feature["status"]=="online":
        online_features=online_features+1
    total_call_count=total_call_count+feature["call_count"]
print(f"功能总数：{len(features)}")
print(f"在线功能数：{online_features}")
print(f"总调用次数：{total_call_count}次")