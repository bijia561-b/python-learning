cost=float(input("请输入成本"))
budget=float(input("请输入预算"))

usage=cost/budget*100

print (f"成本使用率：{usage:.2f}%")

if usage<=80:
    print("成本健康")
elif usage>100:
    print("成本超支，立即排查")
else:
    print("注意成本")