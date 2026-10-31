# Day 3 测验：成本使用率预警器（练习百分比计算与多分支预警判断）

# 输入实际花费成本和总预算（金额用 float 小数）
cost=float(input("请输入成本"))
budget=float(input("请输入预算"))

# 计算预算使用率百分比：实际成本 ÷ 预算 × 100
usage=cost/budget*100

# 打印使用率，保留 2 位小数
print (f"成本使用率：{usage:.2f}%")

# 判断预算使用状态：
# 80% 及以内属于健康
if usage<=80:
    print("成本健康")
# 超过 100% 说明已经超支
elif usage>100:
    print("成本超支，立即排查")
# 其余情况（即 80% < usage <= 100%）提醒注意成本
else:
    print("注意成本")
