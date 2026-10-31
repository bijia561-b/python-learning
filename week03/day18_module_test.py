# Day 18：模块导入练习（用 from ... import ... 从自己的模块里借用函数）

# 从同目录的 cost_utils.py 文件中，导入 usage 和 total_cost 两个函数
from cost_utils import usage,total_cost

# 获取用户输入
cost=float(input("实际成本"))
budget=float(input("预算"))
call_count=int(input("调用次数"))
per_cost=float(input("调用成本"))

# 直接调用导入进来的函数
cost_usage=usage(cost,budget)
total=total_cost(call_count,per_cost)

# 根据返回值是否为 None 输出结果
if cost_usage is None:
    print("预算必须大于0")
else:
    print(f"使用率：{cost_usage:.1f}%")

print(f"成本：{total:.2f}元")
