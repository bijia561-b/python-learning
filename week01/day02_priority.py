# Day 2：AI 项目问题优先级判断器（练习比较运算符 >、==、>= 和逻辑组合）

# 输入受影响的用户数量（整数）和问题严重程度（1到5的整数）
affected_users = int(input("请输入受影响用户数："))
severity = int(input("请输入严重程度（1-5）："))

# == 表示判断两边是否相等（注意：单个 = 是赋值，两个 == 才是比较相等）
# 当受影响人数超过 1000 并且 严重程度等于最高级 5 时，立即处理
if affected_users > 1000 and severity == 5:
    print("立即处理")
# 否则，如果受影响人数超过 500 或者 严重程度达到 3 及以上，安排处理
elif affected_users > 500 or severity >= 3:
    print("安排处理")
# 其余影响较小的情况，放入待办列表
else:
    print("进入待办列表")
