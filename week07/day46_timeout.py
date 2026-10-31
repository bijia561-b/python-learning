# Day 46：接口超时捕获（Timeout）与有限次数重试机制（最多重试 3 次，避免死循环）

import requests

# 这个测试接口会故意延迟 5 秒才返回
url="https://httpbin.org/delay/5"

# 设置最多尝试 3 次
max_times=3
# range(1, max_times + 1) 会依次生成 1, 2, 3
for i in range(1,max_times+1):
    print(f"第{i}次尝试")
    try:
        # timeout=1 表示只等 1 秒，因为对方要 5 秒才回，所以一定会触发 Timeout 异常
        response=requests.get(url,timeout=1)
        # 如果在时限内收到 200 成功响应，打印成功并用 break 立即跳出循环，不再多余重试
        if response.status_code==200:
            print("success200")
            break
        print("fail",response.status_code)
    except requests.exceptions.Timeout:
        # 专门捕获超时异常，给出友好提示而不让程序崩溃
        print("接口超时")
    except requests.exceptions.RequestException as error:
        # 捕获其它网络类异常（如断网、域名无法解析等）
        print("请求失败:",type(error).__name__,error)

    # 如果到了第 3 次（最后一次）还没有 break 跳出，说明 3 次全败，打印最终放弃提示
    if i==max_times:
        print("已达最大次数")
