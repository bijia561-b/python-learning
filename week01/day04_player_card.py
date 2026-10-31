# Day 4：玩家信息卡格式化输出（练习字符串输入与 f-string 排版）

# 依次获取玩家名称、渠道（字符串）以及等级（整数）、充值金额（小数）
name=input("请输入玩家名称")
channel=input("请输入玩家来源渠道")
level=int(input("请输入玩家等级"))
recharge=float(input("请输入累计充值金额"))

# 空的 print() 会打印一个空行，让输出排版更清晰
print()
print("=====玩家信息卡=====")
print(f"玩家名称：{name}")
print(f"来源渠道：{channel}")
print(f"当前等级：{level}")
# :.2f 将充值金额格式化为 2 位小数
print(f"累计充值：{recharge:.2f}元")
print("========================")
