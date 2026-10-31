# Day 23：类的初始化方法 __init__ 与实例方法（让对象不仅有属性，还能执行动作）

class Player:
    # __init__ 是创建对象时自动执行的初始化函数；self 代表“当前正在创建的这个玩家对象自己”
    def __init__(self,name,level,vip,server):
        self.name=name
        self.level=level
        self.vip=vip
        self.server=server

    # 实例方法 1：升级（让自己当前的等级 +1）
    def level_up(self):
        self.level=self.level+1

    # 实例方法 2：展示玩家信息
    def show_info(self):
        print(f"玩家：{self.name},等级：{self.level},服务器：{self.server}")

    # 实例方法 3：充值（接收一个充值金额参数 amount 并打印）
    def recharge(self,amount):
        print(f"{self.name}充值了{amount}元")

# 创建两个玩家对象，括号里的参数会自动传给 __init__
player_1=Player("小林",12,True,1)
player_2=Player("小周",5,False,2)

# 调用升级方法：小林升 1 级，小周连升 2 级
player_1.level_up()
player_2.level_up()
player_2.level_up()

print(f"{player_1.name}的等级：{player_1.level}")
print(f"{player_2.name}的等级：{player_2.level}")

# 调用展示信息和充值方法
player_1.show_info()
player_2.recharge(30)
