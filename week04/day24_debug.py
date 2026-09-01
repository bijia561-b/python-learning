def spend_gold(gold,cost):
    if gold<0 or cost<0 or cost>gold:
        return None
    else:
        return gold+cost

gold=float(input("输入金币："))
cost=float(input("消费金币："))

rest=spend_gold(gold,cost)
print(f"剩余：{rest:.2f}")