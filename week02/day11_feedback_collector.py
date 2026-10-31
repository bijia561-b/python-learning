# Day 11：玩家反馈收集器（练习 while True 无限循环、break 退出与 continue 跳过）

# 先创建一个空列表，用来装用户输入的反馈
feedbacks=[]

# while True 表示一直重复循环，直到遇到 break 才会停下
while True:
    feedback=input("请输入玩家反馈；输入quit结束：")
    # 如果用户输入 quit，用 break 跳出整个 while 循环
    if feedback=="quit":
        break

    # 如果用户直接按回车（输入为空字符串 ""），提示后用 continue 跳过本轮后面的代码，直接开始下一轮输入
    if feedback=="":
        print("反馈不能为空，请重新输入。")
        continue

    # 只有既不是 quit、也不是空字符串时，才会追加到列表中
    feedbacks.append(feedback)
    print("已添加。")

print()
print(f"共收集{len(feedbacks)}条反馈")

# 带编号（从 1 开始）打印所有收集到的反馈
for index,feedback in enumerate(feedbacks,start=1):
    print(f"{index}.{feedback}")
