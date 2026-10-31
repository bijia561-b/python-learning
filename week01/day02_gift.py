# Day 2：玩家礼包推荐器（练习 if/elif/else 条件判断与 and/or 逻辑运算）

# 读取玩家等级（整数）和累计充值金额（小数）
level = int(input("请输入玩家等级："))
recharge = float(input("请输入累计充值金额："))

# if / elif / else 会从上往下依次检查条件，一旦某一条成立，就执行对应代码并跳过后面的分支：
# and 表示“并且”：必须同时满足等级 >= 10 且 充值 >= 100
if level >= 10 and recharge >= 100:
    print("推荐：高级礼包")
# elif 是“否则如果”；or 表示“或者”：只要等级 >= 5 或 充值 >= 50 满足其中一个即可
elif level >= 5 or recharge >= 50:
    print("推荐：普通礼包")
# else 表示上面所有条件都不满足时的默认情况
else:
    print("推荐：新手礼包")
