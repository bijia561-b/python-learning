import os
import time
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

project_dir = Path(__file__).parent
output_dir = project_dir / "output"
output_dir.mkdir(exist_ok=True)
load_dotenv(project_dir / ".env")

INPUT_PRICE_PER_1K = 0.001
OUTPUT_PRICE_PER_1K = 0.004
COST_LIMIT = 0.05
MAX_TRIES = 3
RETRY_STATUS = {429, 500, 502, 503, 504}

def calc_cost(prompt_tokens, completion_tokens):
    return prompt_tokens / 1000 * INPUT_PRICE_PER_1K + completion_tokens / 1000 * OUTPUT_PRICE_PER_1K

print("本地停机演示：")
running = 0
for fake_cost in (0.02, 0.02, 0.02):
    if running >= 0.03:
        print("累计已达演示上限，停止")
        break
    running = round(running + fake_cost, 4)
    print("记入", fake_cost, "累计", running)

key = os.getenv("DEEPSEEK_API_KEY")
if not key:
    print("缺少 DEEPSEEK_API_KEY，已停止，未发送请求")
    raise SystemExit

url = "https://cloud.vtrix.ai/llm/chat/completions"
model = "deepseek-v4.1-flash"
headers = {"Authorization": f"Bearer {key}"}
system_prompt = "你是游戏反馈分类器。只输出一个词：充值、性能、登录、社交、其它。"
feedbacks = [
    "充了 68 元月卡，半小时了还没到账。",
    "进图就卡，掉到 10 帧，没法打。",
    "登录一直转圈，进不去游戏。",
]

def post_with_retry(feedback):
    for attempt in range(1, MAX_TRIES + 1):
        try:
            response = requests.post(
                url,
                headers=headers,
                json={
                    "model": model,
                    "temperature": 0,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": feedback},
                    ],
                },
                timeout=30,
            )
        except requests.exceptions.Timeout:
            print(f"第 {attempt} 次超时")
            if attempt == MAX_TRIES:
                return None, attempt, "timeout"
            time.sleep(1)
            continue
        except requests.exceptions.RequestException as error:
            return None, attempt, type(error).__name__

        if response.status_code == 200 or response.status_code not in RETRY_STATUS:
            return response, attempt, ""
        print(f"第 {attempt} 次状态码 {response.status_code}，准备重试")
        if attempt == MAX_TRIES:
            return response, attempt, "retry_exhausted"
        time.sleep(1)
    return None, MAX_TRIES, "retry_exhausted"

rows = []
total_cost = 0
for feedback in feedbacks:
    if total_cost >= COST_LIMIT:
        print("累计成本达到上限，停止后续请求")
        break
    response, attempts, error = post_with_retry(feedback)
    row = {
        "feedback": feedback,
        "attempts": attempts,
        "status_code": None if response is None else response.status_code,
        "output": "",
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "cost_yuan": 0,
        "error": error,
    }
    if response is not None and response.status_code == 200:
        data = response.json()
        row["output"] = data["choices"][0]["message"]["content"].strip()
        usage = data.get("usage", {})
        row["prompt_tokens"] = usage.get("prompt_tokens") or 0
        row["completion_tokens"] = usage.get("completion_tokens") or 0
        row["cost_yuan"] = round(calc_cost(row["prompt_tokens"], row["completion_tokens"]), 6)
    elif response is not None and not error:
        row["error"] = f"http_{response.status_code}"
    total_cost = round(total_cost + row["cost_yuan"], 6)
    rows.append(row)
    print(row["status_code"], row["attempts"], row["output"], row["cost_yuan"], row["error"])

table = pd.DataFrame(rows)
out_path = output_dir / "day68_cost.csv"
table.to_csv(out_path, index=False, encoding="utf-8-sig")
print("请求条数：", len(table))
print("输入 Token 合计：", int(table["prompt_tokens"].sum()))
print("输出 Token 合计：", int(table["completion_tokens"].sum()))
print("总成本（元）：", round(table["cost_yuan"].sum(), 6))
print("已导出：", out_path)