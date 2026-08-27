feedbacks=[]
while True:
    feedback=input("请输入玩家反馈；输入quit结束：")
    if feedback=="quit":
        break

    if feedback=="":
        print("反馈不能为空，请重新输入。")
        continue

    feedbacks.append(feedback)
    print("已添加。")

print()
print(f"共收集{len(feedbacks)}条反馈")

for index,feedback in enumerate(feedbacks,start=1):
    print(f"{index}.{feedback}")