# Day 16：单一职责原则与函数组合（一个函数只做一件事）

# 函数 1：只负责计算成功率
def calculate_success_rate(success_count, call_count):
    success_rate = success_count / call_count * 100
    return success_rate


# 函数 2：只负责计算总成本
def calculate_total_cost(call_count, per_call_cost):
    total_cost = call_count * per_call_cost
    return total_cost


# 获取用户输入
feature_name = input("请输入功能名称：")
call_count = int(input("请输入调用次数："))
success_count = int(input("请输入成功次数："))
per_call_cost = float(input("请输入单次调用成本："))

# 分别调用两个单一职责的函数，组合出完整报告所需的数据
success_rate = calculate_success_rate(success_count, call_count)
total_cost = calculate_total_cost(call_count, per_call_cost)

print()
print("=== AI 功能报告 ===")
print(f"功能名称：{feature_name}")
print(f"成功率：{success_rate:.1f}%")
print(f"总成本：{total_cost:.2f} 元")
