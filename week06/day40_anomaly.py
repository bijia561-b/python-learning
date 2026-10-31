# Day 40：指标异常检测——使用 pct_change() 计算环比变化率，并标记波动超过 20% 的异常日期

import pandas as pd
from pathlib import Path
input_path="week06/day40_metrics.csv"

table=pd.read_csv(input_path)
table["login_date"]=pd.to_datetime(table["login_date"])

# .pct_change() 自动计算每一天相对于前一天的环比变化比例：(今天 - 昨天) ÷ 昨天
table["dau_change"]=table["dau"].pct_change()
# .abs() 取绝对值（不管暴涨还是暴跌），只要变化幅度超过 0.2（即 20%），就标记为 True（异常报警）
table["dau_alert"]=table["dau_change"].abs()>0.2

print(table[["login_date","dau","revenue","dau_change","dau_alert"]])
print("异常日期")
# 筛选出 dau_alert 为 True 的所有异常行
print(table[table["dau_alert"]][["login_date","dau","revenue","dau_change"]])
