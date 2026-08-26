target=int(input("请输入活动目标参数人数"))
actual=int(input("请输入实际参与人数"))

completion_rate=actual/target*100

print(f"活动完成率:{completion_rate:.1f}%")

if completion_rate >= 100:
	print("结果：已达成或超额完成目标")
elif completion_rate >= 80:
	print("结果：接近目标，建议继续观察")
else:
	print("结果：未达目标，需分析原因")