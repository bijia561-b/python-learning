# Day 44 测验：使用 params 传递参数，并用 if 判断拦截 400 错误响应

import requests

url="https://httpbin.org/get"
# 通过 params 传入 feature 和 env 两个查询参数
response=requests.get(
    url,
    params={"feature":"ai_客服","env":"test"},
    timeout=10
)

print("url:",response.url)
print("状态码：",response.status_code)
print("参数：",response.json()["args"])

# 请求返回 400 状态码的测试接口
r400=requests.get("https://httpbin.org/status/400",timeout=10)
print(r400.status_code)

# 只有状态码为 200 时才解析 JSON，否则提示失败并打印状态码
if r400.status_code==200:
    data=r400.json()
else:
    print("失败",r400.status_code)
