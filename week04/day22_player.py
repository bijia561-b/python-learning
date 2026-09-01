class Player:
    pass

player_1=Player()
player_1.name="小林"
player_1.level=12
player_1.vip=True
player_1.server=1

player_2=Player()
player_2.name="小周"
player_2.level=6
player_2.vip=False
player_2.server=2

player_3=Player()
player_3.name="huey"
player_3.level=8
player_3.vip=True
player_3.server=3

print(f"玩家:{player_1.name},等级：{player_1.level},VIP:{player_1.vip}")
print(f"玩家：{player_2.name},等级：{player_2.level},VIP:{player_2.vip}")