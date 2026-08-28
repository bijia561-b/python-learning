from cost_utils import usage,total_cost

cost=float(input("实际成本"))
budget=float(input("预算"))
call_count=int(input("调用次数"))
per_cost=float(input("调用成本"))

cost_usage=usage(cost,budget)
total=total_cost(call_count,per_cost)

if cost_usage is None:
    print("预算必须大于0")
else:
    print(f"使用率：{cost_usage:.1f}%")

print(f"成本：{total:.2f}元")