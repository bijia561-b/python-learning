# Day 8 测验：AI 问题列表（练习列表操作与 enumerate 带编号遍历）

# 创建包含 5 个问题的列表
issues=["Q1","Q2","Q3","Q4","Q5"]
# 打印列表元素个数
print(f"问题数：{len(issues)}")
# 打印第一个元素（索引为 0）
print(f"第一个问题：{issues[0]}")

# 在列表末尾追加 "Q6"
issues.append("Q6")
print("全部问题：")
# enumerate(issues, start=1) 会在循环时同时给出序号 index（从 1 开始数）和内容 issue
for index, issue in enumerate(issues, start=1):
    print(f"{index}.{issue}")
