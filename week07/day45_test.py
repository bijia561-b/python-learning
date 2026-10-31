# Day 45 测验：调用天气接口，记录耗时、提取嵌套字段并保存为 JSON 文件

import json
import requests
from pathlib import Path

project_dir=Path(__file__).parent
output_dir=project_dir/"output"
output_dir.mkdir(exist_ok=True)
output_path=output_dir/"day45_weather.json"

# 公开天气接口（查询上海经纬度的当前气温）
url="https://api.open-meteo.com/v1/forecast?latitude=31.23&longitude=121.47&current=temperature_2m"
response=requests.get(
    url,
    timeout=10,
)

print("status_code:",response.status_code)
print("time:",response.elapsed.total_seconds())

# 仅在状态码为 200 时提取数据并保存文件
if response.status_code!=200:
    print("fail")
else:
    data=response.json()
    print("latitude",data["latitude"])
    print("longitude",data["longitude"])
    # data["current"]["temperature_2m"] 是嵌套字典取值：先进入 current 字典，再取里面的 temperature_2m
    print("temp",data["current"]["temperature_2m"])
    with output_path.open("w",encoding="utf-8") as file:
        json.dump(data,file,ensure_ascii=False,indent=2)
    print("saved",output_path)
