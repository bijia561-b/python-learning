# Day 24：断点调试练习（用来观察逻辑错误的示例代码）

def spend_gold(gold,cost):
    # 如果初始金币 < 0、消费金币 < 0，或者消费比拥有的金币还多，返回 None 表示无效
    if gold<0 or cost<0 or cost>gold:
        return None
    else:
        # 注意：这里故意把减号 - 写成了加号 +（gold+cost），用于练习打断点调试找出逻辑错误
        return gold+cost

gold=float(input("输入金币："))
cost=float(input("消费金币："))

rest=spend_gold(gold,cost)
print(f"剩余：{rest:.2f}")
