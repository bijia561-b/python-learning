# Day 22：面向对象入门——类（Class）与对象（Object）

# class 用来定义一个“类”（相当于一张设计图纸），pass 表示里面暂时什么都不写
class Player:
    pass

# 用 Player() 根据图纸造出第 1 个具体的玩家对象 player_1，并给它贴上属性（姓名、等级、VIP、区服）
player_1=Player()
player_1.name="小林"
player_1.level=12
player_1.vip=True
player_1.server=1

# 造出第 2 个玩家对象 player_2
player_2=Player()
player_2.name="小周"
player_2.level=6
player_2.vip=False
player_2.server=2

# 造出第 3 个玩家对象 player_3
player_3=Player()
player_3.name="huey"
player_3.level=8
player_3.vip=True
player_3.server=3

# 通过 对象名.属性名 读取并打印玩家信息
print(f"玩家:{player_1.name},等级：{player_1.level},VIP:{player_1.vip}")
print(f"玩家：{player_2.name},等级：{player_2.level},VIP:{player_2.vip}")
