# Day 45：记录接口请求耗时（elapsed）并将返回的 JSON 保存到本地文件

import json
import requests
from pathlib import Path

project_dir=Path(__file__).parent
output_dir=project_dir/"output"
output_dir.mkdir(exist_ok=True)
output_path=output_dir/"day45_httpbin.json"

url="https://httpbin.org/get"
response=requests.get(
    url,
    params={"player":"小林","feature":"ai_客服"},
    timeout=10,
)

print("状态码:",response.status_code)
# response.elapsed.total_seconds() 获取本次请求从发出到收到响应一共花了多少秒
print("耗时秒:",response.elapsed.total_seconds())

# 先检查状态码：如果不是 200，不解析也不保存；如果是 200，取出字段并用 json.dump 存盘
if response.status_code !=200:
    print("请求失败，不保存")
else:
    data=response.json()
    print("url:",data["url"])
    print("origin:",data["origin"])
    print("args:",data["args"])
    # 将字典保存为格式化的 JSON 文件（ensure_ascii=False 保持中文汉字不转码）
    with output_path.open("w",encoding="utf-8") as file:
        json.dump(data,file,ensure_ascii=False,indent=2)
    print("已保存:",output_path)
