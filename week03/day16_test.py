# Day 16 测验：用两个独立函数分别计算活动完成率和成本使用率

# 函数 1：计算活动参与完成率（实际人数 ÷ 目标人数 × 100）
def calculate_completion_rate(actual_count, goal_count):
    completion_rate = actual_count / goal_count * 100
    return completion_rate


# 函数 2：计算成本使用率（实际成本 ÷ 预算 × 100）
def calculate_cost_usage(actual_cost, budget):
    cost_usage = actual_cost / budget * 100
    return cost_usage


# 获取用户输入的活动数据
activity_name = input("请输入活动名称：")
goal_count = int(input("请输入目标人数："))
actual_count = int(input("请输入实际参与人数："))
budget = float(input("请输入活动预算："))
actual_cost = float(input("请输入实际成本："))

# 调用两个函数获取计算结果
completion_rate = calculate_completion_rate(actual_count, goal_count)
cost_usage = calculate_cost_usage(actual_cost, budget)

# 输出复盘报告
print()
print("=== 游戏活动复盘报告 ===")
print(f"活动名称：{activity_name}")
print(f"参与完成率：{completion_rate:.1f}%")
print(f"成本使用率：{cost_usage:.1f}%")
