# Day 4 测验：AI 功能调用报告（综合练习输入、四则运算与 f-string 输出报告）

# 获取功能名称、调用次数、成功次数和单次成本
name=input("请输入功能名称:")
call_count=int(input("请输入调用次数："))
success_count=int(input("请输入成功次数："))
Per_cost=float(input("请输入单次调用成本："))

# 计算成功率（百分比）和总成本
success_rate=success_count/call_count*100
total_cost=call_count*Per_cost

# 打印结构化的调用报告
print("===AI功能调用报告===")
print(f"功能名称：{name}")
print(f"调用次数：{call_count}")
print(f"成功次数：{success_count}")
print(f"成功率：{success_rate:.1f}%")
print(f"总成本：{total_cost:.2f}元")
print("=======")
