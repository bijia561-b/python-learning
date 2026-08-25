price=float(input("请输入单价："))
people=int(input("请输入人数："))
days=int(input("请输入天数："))
budget=price*people*days
print(f"总预算：{budget:.2f}元")
