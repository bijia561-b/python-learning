# Day 1：玩家信息卡（练习变量、input 输入、数据类型转换与格式化输出）

# input() 获取用户输入，默认得到的是字符串（str，即文本）
name = input("请输入玩家名称：")

# int() 把输入的文本转换成整数（int），因为等级是没有小数的整数
level = int(input("请输入玩家等级："))

# float() 把输入的文本转换成浮点数（float，即带小数的数字），因为金额可能有小数
recharge = float(input("请输入累计充值金额："))

# 打印标题
print("玩家信息")
# 使用 f-string 把变量的值拼接到文字中输出
print(f"名称：{name}")
print(f"等级：{level}")
# {recharge:.2f} 中的 :.2f 表示将小数保留 2 位小数输出（例如 99 变成 99.00）
print(f"累计充值：{recharge:.2f} 元")
