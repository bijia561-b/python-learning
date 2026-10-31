# Day 15：函数入门（练习用 def 定义函数并传入参数）

# def 用来定义一个函数（相当于把一段重复要用的代码打包成一个小工具）
# name 和 status 是函数的“参数”（外部调用时传进来的原材料）
def print_feature_info(name,status):
    print(f"功能名称:{name}")
    print(f"运行状态:{status}")
    print()

# 调用函数：直接写函数名并传入具体的值，省去了重复写多遍 print 的麻烦
print_feature_info("玩家反馈分类","online")
print_feature_info("智能客服","offline")
