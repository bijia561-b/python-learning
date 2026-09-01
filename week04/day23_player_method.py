class Player:
    def __init__(self,name,level,vip,server):
        self.name=name
        self.level=level
        self.vip=vip
        self.server=server

    def level_up(self):
        self.level=self.level+1

    def show_info(self):
        print(f"玩家：{self.name},等级：{self.level},服务器：{self.server}")

    def recharge(self,amount):
        print(f"{self.name}充值了{amount}元")

player_1=Player("小林",12,True,1)
player_2=Player("小周",5,False,2)

player_1.level_up()
player_2.level_up()
player_2.level_up()

print(f"{player_1.name}的等级：{player_1.level}")
print(f"{player_2.name}的等级：{player_2.level}")

player_1.show_info()
player_2.recharge(30)