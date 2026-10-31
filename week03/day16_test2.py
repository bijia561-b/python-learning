# Day 16 练习 2：手敲复现活动完成率与成本使用率函数

# 定义完成率函数
def completion_rate(actual_count,goal_count):
    completion_rate=actual_count/goal_count*100
    return completion_rate

# 定义成本使用率函数
def cost_usage(actual_cost,budget):
    cost_usage=actual_cost/budget*100
    return cost_usage

# 获取输入
activity_name=input("活动名称：")
goal_count=int(input("目标人数："))
actual_count=int(input("实际人数："))
actual_cost=float(input("成本："))
budget=float(input("预算："))

# 调用函数（注意：这里把函数返回值赋给了同名变量）
completion_rate=completion_rate(actual_count,goal_count)
cost_usage=cost_usage(actual_cost,budget)

print(f"完成率：{completion_rate:.1f}%")
print(f"成本使用率：{cost_usage:.1f}%")
