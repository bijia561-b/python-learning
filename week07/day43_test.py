# Day 43 测验：调用公开狗狗图片 API，检查状态码并提取 JSON 中的字段

import requests

# 免密钥的公开接口：随机返回一张狗狗图片链接
url="https://dog.ceo/api/breeds/image/random"
# 发送 GET 请求，设置 10 秒超时保护
response=requests.get(url,timeout=10)

# 打印 HTTP 状态码（200 为成功）和原始返回文本
print("状态码：",response.status_code)
print("原始文本：")
print(response.text)

# 将 JSON 文本转为 Python 字典，并取出 status 和 message 两个字段
data=response.json()
print("json里的status:",data["status"])
print("json里的message",data["message"])
