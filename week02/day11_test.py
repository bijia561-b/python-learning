problems=[]
while True:
    problem=input("AI功能问题：")

    if problem=="done":
        break
    if problem=="":
        print("不能为空")
        continue
    problems.append(problem)
    print("已添加")
print()
print(f"总数量:{len(problems)}")
for index,problem in enumerate(problems,start=1):
    print(f"{index}、{problem}")