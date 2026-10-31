# Day 11 测验：AI 问题收集器（练习 while 循环收集非空输入）

# 空列表用于保存收集到的问题
problems=[]
while True:
    problem=input("AI功能问题：")

    # 输入 done 时结束循环
    if problem=="done":
        break
    # 空输入不保存，直接进入下一轮循环
    if problem=="":
        print("不能为空")
        continue
    # 保存有效输入
    problems.append(problem)
    print("已添加")
print()
print(f"总数量:{len(problems)}")
# 从 1 开始编号打印所有问题
for index,problem in enumerate(problems,start=1):
    print(f"{index}、{problem}")
