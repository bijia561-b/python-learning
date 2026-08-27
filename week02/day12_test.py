logs=[
    "调用成功",
    "调用失败",
    "创建失败",
    "连接超时",
    "任务结束",
]

error_logs=[]
for log in logs:
    if "失败" in log or "超时" in log:
        error_logs.append(log)

print(f"异常日志数量：{len(error_logs)}")
for index,log in enumerate(error_logs,start=1):
    print(f"{index}.{log}")


