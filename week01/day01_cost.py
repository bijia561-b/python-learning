price = float(input("请输入单次 AI 调用成本："))
count = int(input("请输入调用次数："))

total_cost = price * count

print(f"预计总成本：{total_cost:.2f} 元")