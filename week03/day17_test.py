# Day 17 测验：带参数校验的预算使用率函数

def usage(cost,budget):
    # 校验分母：如果预算小于等于 0，返回 None 代表无效
    if budget<=0:
        return None
    return cost/budget*100

cost=float(input("成本："))
budget=float(input("预算"))

cost_usage=usage(cost,budget)

# 用 is None 检查是否触发了无效预算拦截
if cost_usage is None:
    print("预算必须大于0")
else:
    print(f"使用率：{cost_usage:.1f}%")
