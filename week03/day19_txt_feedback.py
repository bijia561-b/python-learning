# Day 19：读取 TXT 文本文件（练习 open()、with 自动关闭文件与 splitlines() 按行切分）

# 要读取的 txt 文件路径
file_path="week03/day19_feedback.txt"

# with open(...) as file: 打开文件，代码块结束后会自动关闭文件（防止文件被占用）
# "r" 表示只读模式（read），encoding="utf-8" 防止中文乱码
with open(file_path,"r",encoding="utf-8") as file:
    # .read() 把整个文件的内容读成一个长字符串
    feedback_text=file.read()

# .splitlines() 按换行符把长字符串切分成列表，每一行变成列表里的一个元素
feedback_lines=feedback_text.splitlines()

print("玩家反馈：")

# 逐行打印反馈内容
for line in feedback_lines:
    print(f"-{line}")

# 用 len() 统计一共有多少行反馈
print(f"反馈行数：{len(feedback_lines)}")
