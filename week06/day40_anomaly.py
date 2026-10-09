import pandas as pd
from pathlib import Path
input_path="week06/day40_metrics.csv"

table=pd.read_csv(input_path)
table["login_date"]=pd.to_datetime(table["login_date"])

table["dau_change"]=table["dau"].pct_change()
table["dau_alert"]=table["dau_change"].abs()>0.2

print(table[["login_date","dau","revenue","dau_change","dau_alert"]])
print("异常日期")
print(table[table["dau_alert"]][["login_date","dau","revenue","dau_change"]])