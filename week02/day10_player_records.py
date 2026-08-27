players = [
    {"name": "Ava", "level": 12, "recharge": 120.0},
    {"name": "Ben", "level": 6, "recharge": 30.0},
    {"name": "Chloe", "level": 20, "recharge": 220.0},
]

total_recharge = 0
high_value_count = 0

for player in players:
    print(
        f"玩家：{player['name']}，"
        f"等级：{player['level']}，"
        f"充值：{player['recharge']:.2f} 元"
    )

    total_recharge = total_recharge + player["recharge"]

    if player["recharge"] >= 100:
        high_value_count = high_value_count + 1

print()
print(f"玩家总数：{len(players)}")
print(f"累计充值：{total_recharge:.2f} 元")
print(f"高价值玩家数：{high_value_count}")
