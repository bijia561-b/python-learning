# Day 43：HTTP 请求入门——发送 GET 请求、查看状态码 200 并解析返回的 JSON 数据

# 导入 requests 库，专门用来通过网络向接口（API）发请求
import requests

# 要访问的公开测试接口地址
url="https://httpbin.org/get"
# requests.get() 发送 GET 请求获取数据；timeout=10 表示最多等 10 秒，超时就报错停止，避免程序无限卡死
response=requests.get(url,timeout=10)

# response.status_code 是 HTTP 状态码（200 表示请求成功）
print("状态码：",response.status_code)
# response.text 是服务器返回的原始字符串文本
print("原始文本：")
print(response.text)

# response.json() 把返回的 JSON 格式文本转换成 Python 字典，方便直接用 ["键名"] 取值
data=response.json()
print("json里的url:",data["url"])
print("json里的origin:",data["origin"])
