# Day 2 测验：根据影响人数和严重程度判断处理优先级

# 读取受影响用户数（int 整数）和严重程度（int 整数）
people = int(input("请输入影响用户数："))
severity=int(input("请输入严重程度："))

# 条件 1：人数 > 1000 且 严重程度 == 5（最紧急，必须优先判断）
if people > 1000 and severity == 5:
	print("立即处理")
# 条件 2：人数 > 500 或 严重程度 >= 3（次紧急）
elif people>500 or severity >=3:
	print("安排处理")
# 以上都不满足时，归入待办列表
else:
	print("进入待办列表")
