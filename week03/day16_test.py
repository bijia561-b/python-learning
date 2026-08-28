def calculate_completion_rate(actual_count, goal_count):
    completion_rate = actual_count / goal_count * 100
    return completion_rate


def calculate_cost_usage(actual_cost, budget):
    cost_usage = actual_cost / budget * 100
    return cost_usage


activity_name = input("请输入活动名称：")
goal_count = int(input("请输入目标人数："))
actual_count = int(input("请输入实际参与人数："))
budget = float(input("请输入活动预算："))
actual_cost = float(input("请输入实际成本："))

completion_rate = calculate_completion_rate(actual_count, goal_count)
cost_usage = calculate_cost_usage(actual_cost, budget)

print()
print("=== 游戏活动复盘报告 ===")
print(f"活动名称：{activity_name}")
print(f"参与完成率：{completion_rate:.1f}%")
print(f"成本使用率：{cost_usage:.1f}%")
