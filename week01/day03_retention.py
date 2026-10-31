# Day 3：活动参与完成率计算（练习除法 /、百分比换算与 :.1f 格式化）

# 输入活动目标人数和实际参与人数（均转为整数）
target=int(input("请输入活动目标参数人数"))
actual=int(input("请输入实际参与人数"))

# Python 中 / 是除法，结果会自动变成小数；乘以 100 换算成百分比数值
completion_rate=actual/target*100

# :.1f 表示保留 1 位小数，后面的 % 是普通字符，用来显示百分号
print(f"活动完成率:{completion_rate:.1f}%")

# 根据完成率区间给出业务结论
if completion_rate >= 100:
	print("结果：已达成或超额完成目标")
elif completion_rate >= 80:
	print("结果：接近目标，建议继续观察")
else:
	print("结果：未达目标，需分析原因")
