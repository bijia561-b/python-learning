# Day 48 测验：在调用日志中增加 timeout_limit 字段，并统计成功与失败行数

from datetime import datetime
from pathlib import Path

import pandas as pd
import requests

project_dir=Path(__file__).parent
output_dir=project_dir/"output"
output_dir.mkdir(exist_ok=True)
output_path=output_dir/"day48_call_log_v2.csv"

targets=[
    "https://httpbin.org/get",
    "https://httpbin.org/status/404",
    "https://httpbin.org/delay/5",
]

logs=[]

for url in targets:
    # 初始化日志字典，增加 timeout_limit 字段记录本次设定的超时上限
    row={
        "requested_at":datetime.now().isoformat(timespec="seconds"),
        "url":url,
        "status_code":None,
        "elapsed_seconds":None,
        "ok":False,
        "error":"",
        "timeout_limit":None,
    }
    timeout=1 if "delay" in url else 10
    try:
        response=requests.get(url,timeout=timeout)
        row["status_code"]=response.status_code
        row["elapsed_seconds"]=round(response.elapsed.total_seconds(),3)
        row["ok"]=response.status_code==200
        row["timeout_limit"]=timeout
    except requests.exceptions.Timeout:
        row["error"]="timeout"
    except requests.exceptions.RequestException as error:
        row["error"]=type(error).__name__
    logs.append(row)
    print(row)

table=pd.DataFrame(logs)
table.to_csv(output_path,index=False,encoding="utf-8-sig")

# 在布尔列上 .sum() 会把 True 当作 1、False 当作 0 求和，从而算出成功行数；~table["ok"] 表示对布尔值取反（统计失败行数）
success=table["ok"].sum()
fail=(~table["ok"]).sum()
print("已导出:",output_path)
print(table)
print("success:",int(success),"行")
print("fail:",int(fail),"行")
