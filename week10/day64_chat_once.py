import os
import requests
from pathlib import Path
from dotenv import load_dotenv

project_dir=Path(__file__).parent
load_dotenv(project_dir/".env")

key=os.getenv("DEEPSEEK_API_KEY")
if not key:
    print("缺少DEEPSEEK_API_KEY,已停止,未发送请求")
else:
    response = requests.post(
        "https://cloud.vtrix.ai/llm/chat/completions",
        headers={"Authorization":f"Bearer {key}"},
        json={
            "model":"deepseek-v4.1-flash",
            "temperature":0,
            "messages":[
                {"role":"system","content":"你是游戏反馈分类器。只输出一个词:充值、性能、登录、社交、其它。"},
                {"role":"user","content":"充了68元月卡,半小时了还没到账。"}
            ],
        },
        timeout=30,
    )
    print("状态码：",response.status_code)
    print("耗时秒：",round(response.elapsed.total_seconds(),3))
    if response.status_code !=200:
        print("请求失败,不解析回复")
    else:
        data=response.json()
        print("模型输出：",data["choices"][0]["message"]["content"])
        usage=data.get("usage",{})
        print("输入token:",usage.get("prompt_tokens"))
        print("输出token:",usage.get("completion_tokens"))