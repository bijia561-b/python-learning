feature_name = input("请输入功能名称：")
call_count = int(input("请输入调用次数："))
success_count = int(input("请输入成功次数："))
per_call_cost = float(input("请输入单次调用成本："))

if call_count <= 0:
    print("调用次数必须大于 0，无法计算成功率。")
elif success_count < 0 or success_count > call_count:
    print("成功次数必须在 0 到调用次数之间。")
elif per_call_cost < 0:
    print("单次调用成本不能小于 0。")
else:
    success_rate = success_count / call_count * 100
    total_cost = call_count * per_call_cost

    print()
    print("=== AI 功能调用报告 ===")
    print(f"功能名称：{feature_name}")
    print(f"成功率：{success_rate:.1f}%")
    print(f"总成本：{total_cost:.2f} 元")
