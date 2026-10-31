# Day 18：独立工具模块 cost_utils.py（专门存放成本相关的计算函数，供别的文件 import 导入使用）

# 计算预算使用率（若预算 <= 0 则返回 None）
def usage(cost,budget):
    if budget<=0:
        return None
    return cost/budget*100

# 计算总调用成本（调用次数 × 单次成本）
def total_cost(call_count,per_cost):
    return call_count*per_cost
