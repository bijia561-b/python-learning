# input() 会暂停程序，等待用户在终端输入文字，并把输入的内容（字符串类型）保存到变量 name 中
name = input("请输入你的名字：")

# f"..." 是格式化字符串（f-string），花括号 {name} 会自动替换成变量 name 里的值
print(f"你好，{name}！")

# print() 用于把括号里的文字打印到终端屏幕上
print("Python learning started.")
