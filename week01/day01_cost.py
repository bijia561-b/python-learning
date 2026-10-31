# Day 1：AI 成本计算器（练习 float 小数、int 整数和乘法运算）

# 单次调用成本可能带小数（如 0.02 元），所以用 float() 转为浮点数
price = float(input("请输入单次 AI 调用成本："))

# 调用次数是整数，所以用 int() 转为整数
count = int(input("请输入调用次数："))

# 用 * 号做乘法：总成本 = 单价 × 次数
total_cost = price * count

# :.2f 表示保留 2 位小数打印结果
print(f"预计总成本：{total_cost:.2f} 元")
