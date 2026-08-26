budget = float(input("请输入总预算："))
actual_cost = float(input("请输入实际成本："))

if budget <= 0:
    print("预算必须大于 0。")
else:
    usage_rate = actual_cost / budget * 100
    print(f"成本使用率：{usage_rate:.1f}%")
