people = int(input("请输入影响用户数："))
severity=int(input("请输入严重程度："))

if people > 1000 and severity == 5:
	print("立即处理")
elif people>500 or severity >=3:
	print("安排处理")
else:
	print("进入待办列表")