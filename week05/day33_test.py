import pandas as pd
file_path="week05/day33_login_data.csv"

table=pd.read_csv(file_path)

table["login_date"]=pd.to_datetime(table["login_date"])

gmv=table.groupby("login_date")["recharge"].sum()
dau=table.groupby("login_date")["player"].nunique()

print(gmv)
print(dau)
best_day=gmv.idxmax()

print(f"收入最高的一天：{gmv.idxmax()},收入为{gmv.max()}")
print("活跃人数为：",dau[best_day])