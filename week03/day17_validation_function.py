# Day 17：函数中的参数校验与 None（用 None 表示“无法计算/无效结果”）

def rate(success,call):
    # 如果分母 call <= 0，无法做除法，返回特殊空值 None 表示计算失败
    if call<=0:
        return None
    # 参数合法时，正常返回百分比结果
    return success/call*100

success=int(input("成功："))
call=int(input("调用"))

# 调用函数
success_rate=rate(success,call)

# 判断返回值是不是 None，专门用 is None（不要用 == None）
if success_rate is None:
    print("调用次数必须>0")
else:
    print(f"成功率：{success_rate:.1f}%")
