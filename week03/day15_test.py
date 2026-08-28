def calculate_success_rate(success_count,call_count):
    success_rate=success_count/call_count*100
    return success_rate
success_count=int(input("请输入成功次数："))
call_count=int(input("请输入调用次数："))

success_rate=calculate_success_rate(success_count,call_count)
print(f"成功率：{success_rate:.1f}%")