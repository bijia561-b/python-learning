# Day 10：玩家记录与充值累计（练习遍历字典列表、金额累加与条件计数）

# 列表中保存多位玩家的字典记录
players = [
    {"name": "Ava", "level": 12, "recharge": 120.0},
    {"name": "Ben", "level": 6, "recharge": 30.0},
    {"name": "Chloe", "level": 20, "recharge": 220.0},
]

# 初始化累计充值总额为 0，高价值玩家人数为 0
total_recharge = 0
high_value_count = 0

# 逐个遍历玩家字典
for player in players:
    print(
        f"玩家：{player['name']}，"
        f"等级：{player['level']}，"
        f"充值：{player['recharge']:.2f} 元"
    )

    # 把当前玩家的充值金额加到总金额里
    total_recharge = total_recharge + player["recharge"]

    # 如果充值满 100 元，高价值玩家人数加 1
    if player["recharge"] >= 100:
        high_value_count = high_value_count + 1

print()
print(f"玩家总数：{len(players)}")
print(f"累计充值：{total_recharge:.2f} 元")
print(f"高价值玩家数：{high_value_count}")
