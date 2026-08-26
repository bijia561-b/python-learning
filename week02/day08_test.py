issues=["Q1","Q2","Q3","Q4","Q5"]
print(f"问题数：{len(issues)}")
print(f"第一个问题：{issues[0]}")

issues.append("Q6")
print("全部问题：")
for index, issue in enumerate(issues, start=1):
    print(f"{index}.{issue}")