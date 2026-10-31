# Day 46 测验：对比正常接口（1 次成功）与慢接口（超时重试 3 次后放弃）

import requests

url1 = "https://httpbin.org/get"
url2 = "https://httpbin.org/delay/5"

# 1. 请求正常接口（timeout=10 秒足够），正常拿到 200 和耗时
response1 = requests.get(url1, timeout=10)
print("url1 状态码:", response1.status_code)
print("url1 耗时:", response1.elapsed.total_seconds())

# 2. 请求慢接口（对方需 5 秒，我们只给 timeout=1 秒），最多重试 3 次
max_times = 3
for i in range(1, max_times + 1):
    print(f"第{i}次尝试")
    try:
        response2 = requests.get(url2, timeout=1)
        if response2.status_code == 200:
            print("success200", response2.elapsed.total_seconds())
            break
        print("fail", response2.status_code)
    except requests.exceptions.Timeout:
        print("超时")
    except requests.exceptions.RequestException as error:
        print("请求失败:", type(error).__name__)
    if i == max_times:
        print("已达最大次数，放弃")
