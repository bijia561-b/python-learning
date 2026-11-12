import json
import os
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

project_dir = Path(__file__).parent
load_dotenv(project_dir / ".env")

key = os.getenv("DEEPSEEK_API_KEY")
if not key:
    print("缺少 DEEPSEEK_API_KEY，已停止，未发送请求")
    raise SystemExit

url = "https://cloud.vtrix.ai/llm/chat/completions"
model = "deepseek-v4.1-flash"
messages = [
    {"role": "system", "content": "你是游戏客服。用两句话说明充值未到账时玩家该做什么。不要编造补偿或秒到账。"},
    {"role": "user", "content": "充了 68 元月卡，半小时了还没到账。"},
]
headers = {"Authorization": f"Bearer {key}"}

def call_normal():
    started = time.perf_counter()
    response = requests.post(
        url,
        headers=headers,
        json={"model": model, "temperature": 0, "messages": messages},
        timeout=60,
    )
    elapsed = time.perf_counter() - started
    response.raise_for_status()
    text = response.json()["choices"][0]["message"]["content"]
    return text, elapsed

def call_stream():
    started = time.perf_counter()
    first_seconds = None
    parts = []
    saw_done = False
    response = requests.post(
        url,
        headers=headers,
        json={"model": model, "temperature": 0, "messages": messages, "stream": True},
        timeout=60,
        stream=True,
    )
    response.raise_for_status()
    response.encoding = "utf-8"
    print("流式输出：")
    for line in response.iter_lines(decode_unicode=True):
        if not line or not line.startswith("data:"):
            continue
        payload = line[len("data:"):].strip()
        if payload == "[DONE]":
            saw_done = True
            break
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            continue
        choices = data.get("choices") or []
        if not choices:
            continue
        piece = (choices[0].get("delta") or {}).get("content") or ""
        if not piece:
            continue
        if first_seconds is None:
            first_seconds = time.perf_counter() - started
        print(piece, end="", flush=True)
        parts.append(piece)
    print()
    elapsed = time.perf_counter() - started
    return "".join(parts), elapsed, first_seconds, saw_done

normal_text, normal_seconds = call_normal()
stream_text, stream_seconds, first_seconds, saw_done = call_stream()

print("\n非流式整段：")
print(normal_text)
print("首字耗时秒：", None if first_seconds is None else round(first_seconds, 3))
print("流式总耗时秒：", round(stream_seconds, 3))
print("非流式总耗时秒：", round(normal_seconds, 3))
print("看到结束标记：", saw_done)
print("两段是否相同：", stream_text == normal_text)
print("非流式字数：", len(normal_text), "流式字数：", len(stream_text))