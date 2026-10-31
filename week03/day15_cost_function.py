# Day 15：带返回值的成本计算函数（练习 return 返回计算结果）

# 定义计算总成本的函数，接收调用次数 call_count 和单次成本 per_call_cost
def calculate_total_cost(call_count,per_call_cost):
    total_cost=call_count*per_call_cost
    # return 会把算出来的结果交回给调用这个函数的地方
    return total_cost

# 获取用户输入
call_count=int(input("请输入调用次数："))
per_call_cost=float(input("请输入单词调用成本："))

# 调用函数，并用变量 total_cost 接住函数 return 出来的返回值
total_cost=calculate_total_cost(call_count,per_call_cost)

print(f"总成本：{total_cost:.2f}元")
