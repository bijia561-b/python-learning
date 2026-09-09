import pandas as pd
file_path="week05/day29_activity_data.csv"
activity_data=pd.read_csv(file_path)
print("完整表格：")
print(activity_data)

print("前3行:")
print(activity_data.head(3))

recharge_column=activity_data["recharge"]

print("充值列：")
print(recharge_column)

xx=activity_data["player"]

print("玩家")
print(xx)