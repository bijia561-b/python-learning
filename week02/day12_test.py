# Day 12 测验：筛选失败和超时日志（练习 in 包含判断过滤异常日志）

# 原始运行日志列表
logs=[
    "调用成功",
    "调用失败",
    "创建失败",
    "连接超时",
    "任务结束",
]

# 存放筛选出的异常日志
error_logs=[]
for log in logs:
    # 只要日志包含“失败”或者“超时”，就加入异常日志列表
    if "失败" in log or "超时" in log:
        error_logs.append(log)

print(f"异常日志数量：{len(error_logs)}")
for index,log in enumerate(error_logs,start=1):
    print(f"{index}.{log}")
