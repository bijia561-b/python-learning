level = int(input("请输入玩家等级："))
recharge = float(input("请输入累计充值金额："))

if level >= 10 and recharge >= 100:
    print("推荐：高级礼包")
elif level >= 5 or recharge >= 50:
    print("推荐：普通礼包")
else:
    print("推荐：新手礼包")
