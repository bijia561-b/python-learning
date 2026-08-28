file_path="week03/day19_feedback.txt"

with open(file_path,"r",encoding="utf-8") as file:
    feedback_text=file.read()
feedback_lines=feedback_text.splitlines()

print("玩家反馈：")

for line in feedback_lines:
    print(f"-{line}")

print(f"反馈行数：{len(feedback_lines)}")