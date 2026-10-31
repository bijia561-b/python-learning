# Day 7：第 1 周综合测验——游戏活动复盘与成本预警程序

# 1. 获取用户输入的基础数据
name=input("活动名称：")
goal_count=int(input("目标人数："))
actual_count=int(input("参与人数："))
budget=float(input("预算："))
cost=float(input("成本："))

# 2. 校验输入数据是否合法（拦截小于等于 0 的分母或负数）
if goal_count<=0:
    print("目标人数必须大于0")
elif actual_count<0:
    print("实际参与人数不能小于0")
elif budget<=0:
    print("活动预算必须大于0")
elif cost<0:
    print("实际成本不能小于0")
else:
    # 3. 数据合法时，计算活动完成率和成本使用率
    finish_rate=actual_count/goal_count*100
    useage=cost/budget*100
    print(f"活动名称：{name}")
    print(f"活动完成率：{finish_rate:.1f}%")
    print(f"成本使用率：{useage:.1f}%")

    # 4. 判断参与目标是否达成
    if finish_rate>=100:
        print("参与目标达成")
    else:
        print("参与目标未达成")

    # 5. 判断成本使用状态
    if useage<=80:
        print("成本健康")
    elif useage>100:
        print("成本超支")
    else:
        print("注意成本")
