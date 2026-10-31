# Day 9：玩家信息字典（练习 dict 字典的取值、修改字段、新增字段与 .items() 遍历）

# 用花括号 {} 创建字典（dict），里面是一对对的 "键(key)": 值(value)
player={
    "id":"P001",
    "name":"huey",
    "level":"12",
    "channel":"taptap",
    "recharge":99.9,
    }

# 通过 字典名['键名'] 取出对应的值
print(f"玩家名称：{player['name']}")
print(f"玩家等级：{player['level']}")
print(f"充值金额：{player['recharge']}")

# 如果键名 'level' 已存在，给它赋值就会覆盖修改原来的值
player["level"]=13
# 如果键名 'vip' 原来不存在，给它赋值就会在字典里新增这个字段
player["vip"]=True

print()
print("更新后的玩家信息")
# .items() 会同时取出字典里的每一个键（key）和值（value）
for key,value in player.items():
    print(f"{key}:{value}")
