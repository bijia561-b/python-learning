import pandas as pd
from pathlib import Path

file_path="week06/output/day35_cleaned.csv"
table=pd.read_csv(file_path)
table["login_date"]=pd.to_datetime(table["login_date"]).dt.date
days=sorted(table["login_date"].unique())
day8=table[table["login_date"]==days[0]]
pay_rate8=(
    day8[day8["recharge"]>0]["player"].nunique()/day8["player"].nunique()
)
print("8号充值率:",f"{pay_rate8*100:.1f}%")

day9=table[table["login_date"]==days[1]]
pay_rate9=(
    day9[day9["recharge"]>0]["player"].nunique()/day9["player"].nunique()
)
print("9号充值率:",f"{pay_rate9*100:.1f}%")

day10=table[table["login_date"]==days[2]]
pay_rate10=(
    day10[day10["recharge"]>0]["player"].nunique()/day10["player"].nunique()
)
print("10号充值率:",f"{pay_rate10*100:.1f}%")

rates=pd.Series({
    days[0]:pay_rate8,
    days[1]:pay_rate9,
    days[2]:pay_rate10,
})
print("付费率最高的一天:",rates.idxmax())
print("付费率：",f"{rates.max()*100:.1f}%")

day9_login=set(table[table["login_date"]==days[1]]["player"].unique())
day10_login=set(table[table["login_date"]==days[2]]["player"].unique())
stayed=day9_login&day10_login
print("留存人员:",stayed)
print("9号留存",f"{len(stayed)/len(day9_login)*100:.1f}%")