# Day 44：URL 查询参数（params）与 HTTP 错误状态码（400、404）处理

import requests

url = "https://httpbin.org/get"
# params={...} 会自动把字典拼接到网址问号 ? 后面（如 ?player=小林&channel=抖音），并对中文自动编码
response = requests.get(
    url,
    params={"player": "小林", "channel": "抖音"},
    timeout=10,
)

# response.url 可以看到拼接编码后的完整请求网址
print("实际请求的URL：", response.url)
print("状态码：", response.status_code)
# httpbin 会把收到的查询参数放在 JSON 的 "args" 字段里返回给我们核对
print("对方收到的参数：", response.json()["args"])

# 访问故意返回 404（资源不存在）的测试地址；注意 requests 遇到 404 不会自动崩溃，会正常返回 response 对象
r404 = requests.get("https://httpbin.org/status/404", timeout=10)
print("404练习 状态码：", r404.status_code)
print("404练习 正文：", r404.text)

# 访问故意返回 400（请求参数/格式错误）的测试地址
r400=requests.get("https://httpbin.org/status/400",timeout=10)
print("400练习 状态码：",r400.status_code)

# 安全好习惯：先判断状态码是不是 200，只有等于 200 时才调 .json() 解析数据
if r404.status_code==200:
    data=r404.json()
else:
    print("请求失败，状态码:",r404.status_code)
