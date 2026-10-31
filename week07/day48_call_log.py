# Day 48：记录 API 调用日志（时间、URL、状态码、耗时、是否成功、错误原因）并导出为 CSV

from datetime import datetime
from pathlib import Path

import pandas as pd
import requests

project_dir=Path(__file__).parent
output_dir=project_dir/"output"
output_dir.mkdir(exist_ok=True)
output_path=output_dir/"day48_call_log.csv"

# 准备 3 个测试地址：正常 200、404 失败、5 秒延迟超时
targets=[
    "https://httpbin.org/get",
    "https://httpbin.org/status/404",
    "https://httpbin.org/delay/5",
]

# 用来收集每次调用日志字典的列表
logs=[]

for url in targets:
    # 先初始化一条日志记录，datetime.now().isoformat(timespec="seconds") 生成精确到秒的当前时间字符串
    row={
        "requested_at":datetime.now().isoformat(timespec="seconds"),
        "url":url,
        "status_code":None,
        "elapsed_seconds":None,
        "ok":False,
        "error":"",
    }
    # 如果网址里含 delay 就设 1 秒超时（故意触发超时），否则设 10 秒超时
    timeout=1 if "delay" in url else 10
    try:
        response=requests.get(url,timeout=timeout)
        row["status_code"]=response.status_code
        row["elapsed_seconds"]=round(response.elapsed.total_seconds(),3)
        # 只有状态码等于 200 时 ok 才为 True
        row["ok"]=response.status_code==200
    except requests.exceptions.Timeout:
        # 超时没有响应对象，status_code 保持为空，在 error 列记下 "timeout"
        row["error"]="timeout"
    except requests.exceptions.RequestException as error:
        row["error"]=type(error).__name__

    # 无论成功还是失败，都把这行日志追加到 logs 列表中
    logs.append(row)
    print(row)

# 把日志列表转成 DataFrame 表格并导出为 CSV 文件
table=pd.DataFrame(logs)
table.to_csv(output_path,index=False,encoding="utf-8-sig")
print("已导出:",output_path)
print(table)
