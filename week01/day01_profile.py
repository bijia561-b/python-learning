name = input("请输入玩家名称：")
level = int(input("请输入玩家等级："))
recharge = float(input("请输入累计充值金额："))

print("玩家信息")
print(f"名称：{name}")
print(f"等级：{level}")
print(f"累计充值：{recharge:.2f} 元")
