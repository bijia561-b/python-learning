import pandas as pd
file_path="week05/day29_activity_data.csv"

table=pd.read_csv(file_path)

table1=table[table["recharge"] != 0]

table2=table1.groupby("channel")["recharge"].sum()

print("收入最高的渠道是：",table2.idxmax(),"，","共",table2.max())

table3=table1.groupby("channel")["recharge"].mean()
print("人均最高的渠道：",table3.idxmax())
