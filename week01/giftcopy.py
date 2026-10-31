# Day 2 备份练习：玩家礼包推荐器（同 day02_gift.py）

# 输入等级（整数）与累计充值（小数）
level = int(input("请输入玩家等级："))
recharge = float(input("请输入累计充值金额："))

# 先判断最高档条件（and：两个条件都要满足）
if level >= 10 and recharge >= 100:
    print("推荐：高级礼包")
# 再判断中间档条件（or：满足任意一个即可）
elif level >= 5 or recharge >= 50:
    print("推荐：普通礼包")
# 都不满足则推荐新手礼包
else:
    print("推荐：新手礼包")
