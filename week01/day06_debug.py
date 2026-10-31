# Day 6：报错定位与修复练习（修复后的正确代码）

# 输入总预算和实际成本
budget = float(input("请输入总预算："))
actual_cost = float(input("请输入实际成本："))

# 先判断分母 budget 是否大于 0，避免除以 0 报错
if budget <= 0:
    print("预算必须大于 0。")
else:
    # 计算并打印成本使用率
    usage_rate = actual_cost / budget * 100
    print(f"成本使用率：{usage_rate:.1f}%")
