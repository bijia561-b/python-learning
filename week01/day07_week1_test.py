name=input("活动名称：")
goal_count=int(input("目标人数："))
actual_count=int(input("参与人数："))
budget=float(input("预算："))
cost=float(input("成本："))

if goal_count<=0:
    print("目标人数必须大于0")
elif actual_count<0:
    print("实际参与人数不能小于0")
elif budget<=0:
    print("活动预算必须大于0")
elif cost<0:
    print("实际成本不能小于0")
else:
    finish_rate=actual_count/goal_count*100
    useage=cost/budget*100
    print(f"活动名称：{name}")
    print(f"活动完成率：{finish_rate:.1f}%")
    print(f"成本使用率：{useage:.1f}%")
    if finish_rate>=100:
        print("参与目标达成")
    else:
        print("参与目标未达成")

    if useage<=80:
        print("成本健康")
    elif useage>100:
        print("成本超支")
    else:
        print("注意成本")