logs=[
    "成功1",
    "成功2",
    "成功3",
    "失败1",
    "失败2",
    "超时1",
]

logs_count={
    "成功次数":0,
    "失败次数":0,
    "超时次数":0,
}

for log in logs:
    if "成功" in log:
        logs_count["成功次数"]=logs_count["成功次数"]+1
    elif "失败" in log:
        logs_count["失败次数"]=logs_count["失败次数"]+1
    else:
        logs_count["超时次数"]=logs_count["超时次数"]+1

print("AI调用日志统计：")
for category,count in logs_count.items():
    print(f"{category}-{count}次")