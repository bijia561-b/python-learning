def calculate_total_cost(call_count,per_call_cost):
    total_cost=call_count*per_call_cost
    return total_cost

call_count=int(input("请输入调用次数："))
per_call_cost=float(input("请输入单词调用成本："))

total_cost=calculate_total_cost(call_count,per_call_cost)

print(f"总成本：{total_cost:.2f}元")