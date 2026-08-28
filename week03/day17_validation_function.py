def rate(success,call):
    if call<=0:
        return None
    return success/call*100
success=int(input("成功："))
call=int(input("调用"))

success_rate=rate(success,call)

if success_rate is None:
    print("调用次数必须>0")
else:
    print(f"成功率：{success_rate:.1f}%")