# Day 1 测验：活动预算计算器（练习多变量连乘与小数格式化）

# 获取单价并转为小数（float）
price=float(input("请输入单价："))
# 获取人数并转为整数（int）
people=int(input("请输入人数："))
# 获取天数并转为整数（int）
days=int(input("请输入天数："))

# 总预算 = 单价 × 人数 × 天数
budget=price*people*days

# 打印总预算，:.2f 表示保留两位小数
print(f"总预算：{budget:.2f}元")
