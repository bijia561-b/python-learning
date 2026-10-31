# Day 47：使用 .env 文件与环境变量安全读取 API Key（绝不把密钥硬编码在代码里）

import os
import requests
from pathlib import Path
# load_dotenv 用于把 .env 文件里的键值对加载到系统环境变量中
from dotenv import load_dotenv

project_dir=Path(__file__).parent
# 加载同目录下的 .env 文件
load_dotenv(project_dir/".env")

# os.getenv() 从环境变量中读取密钥；如果没配则返回 None
key=os.getenv("demo_api_key")
if not key:
    # 没读到密钥时直接提示并停止，不要带着空密钥去发请求
    print("缺少DEMO_API_LEY,请检查.env")
else:
    # 安全脱敏打印：只打印密钥长度和最后 4 位（key[-4:]），不打印完整密钥
    print("密钥已加载，长度:",len(key),"末四位：",key[-4:])
    # 通过 headers 请求头把密钥传给对方服务器
    response=requests.get(
        "https://httpbin.org/get",
        headers={"Authorization":f"Bearer{key}"},
        timeout=10
    )
    print("status_code:",response.status_code)
    if response.status_code==200:
        # 查看对方服务器实际收到的 Authorization 请求头内容
        print("authorization:",response.json()["headers"].get("Authorization"))
