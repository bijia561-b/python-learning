def usage(cost,budget):
    if budget<=0:
        return None
    return cost/budget*100

cost=float(input("成本："))
budget=float(input("预算"))

cost_usage=usage(cost,budget)

if cost_usage is None:
    print("预算必须大于0")
else:
    print(f"使用率：{cost_usage:.1f}%")