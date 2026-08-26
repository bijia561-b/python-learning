name=input("请输入功能名称:")
call_count=int(input("请输入调用次数："))
success_count=int(input("请输入成功次数："))
Per_cost=float(input("请输入单次调用成本："))

success_rate=success_count/call_count*100
total_cost=call_count*Per_cost

print("===AI功能调用报告===")
print(f"功能名称：{name}")
print(f"调用次数：{call_count}")
print(f"成功次数：{success_count}")
print(f"成功率：{success_rate:.1f}%")
print(f"总成本：{total_cost:.2f}元")
print("=======")
