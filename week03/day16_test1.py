# Day 16 练习 1：手敲复现 AI 功能成功率和总成本两个计算函数

# 定义成功率计算函数
def calculate_success_rate(success_count,call_count):
    success_rate=success_count/call_count*100
    return success_rate

# 定义总成本计算函数
def calculate_total_cost(call_count,per_call_cost):
    total_cost=call_count*per_call_cost
    return total_cost

# 读取输入参数
feature_name=input("请输入功能名称：")
call_count=int(input("请输入调用次数："))
success_count=int(input("请输入成功次数："))
per_call_cost=float(input("请输入单次调用成本："))

# 调用函数得到结果
success_rate=calculate_success_rate(success_count,call_count)
total_cost=calculate_total_cost(call_count,per_call_cost)

# 打印报告
print()
print("===AI功能报告===")
print(f"功能名称：{feature_name}")
print(f"成功率：{success_rate:.1f}%")
print(f"总成本：{total_cost:.2f}元")
