player={
    "id":"P001",
    "name":"huey",
    "level":"12",
    "channel":"taptap",
    "recharge":99.9,
    }

print(f"玩家名称：{player['name']}")
print(f"玩家等级：{player['level']}")
print(f"充值金额：{player['recharge']}")

player["level"]=13
player["vip"]=True

print()
print("更新后的玩家信息")
for key,value in player.items():
    print(f"{key}:{value}")