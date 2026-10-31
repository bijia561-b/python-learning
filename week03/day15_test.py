# Day 15 测验：编写计算成功率的函数

# 定义函数 calculate_success_rate，接收成功次数和总调用次数，返回成功率百分比
def calculate_success_rate(success_count,call_count):
    success_rate=success_count/call_count*100
    return success_rate

# 获取用户输入的成功次数与总调用次数
success_count=int(input("请输入成功次数："))
call_count=int(input("请输入调用次数："))

# 调用函数并接收返回的成功率
success_rate=calculate_success_rate(success_count,call_count)
# 打印成功率，保留 1 位小数
print(f"成功率：{success_rate:.1f}%")
