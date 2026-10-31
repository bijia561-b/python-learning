# Day 5：输入校验与无效数据拦截（先检查数据合不合理，再做计算）

# 读取各项输入数据
feature_name = input("请输入功能名称：")
call_count = int(input("请输入调用次数："))
success_count = int(input("请输入成功次数："))
per_call_cost = float(input("请输入单次调用成本："))

# 校验 1：调用次数如果 <= 0，后面做除法 call_count 作分母会报错（ZeroDivisionError）或无意义
if call_count <= 0:
    print("调用次数必须大于 0，无法计算成功率。")
# 校验 2：成功次数不能是负数，也不可能比总调用次数还多
elif success_count < 0 or success_count > call_count:
    print("成功次数必须在 0 到调用次数之间。")
# 校验 3：单次成本不能为负数
elif per_call_cost < 0:
    print("单次调用成本不能小于 0。")
# 当所有校验都通过时，才进入 else 计算并输出报告
else:
    success_rate = success_count / call_count * 100
    total_cost = call_count * per_call_cost

    print()
    print("=== AI 功能调用报告 ===")
    print(f"功能名称：{feature_name}")
    print(f"成功率：{success_rate:.1f}%")
    print(f"总成本：{total_cost:.2f} 元")
