import os
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

project_dir = Path(__file__).parent
output_dir = project_dir / "output"
output_dir.mkdir(exist_ok=True)
load_dotenv(project_dir / ".env")

key = os.getenv("DEEPSEEK_API_KEY")
if not key:
    print("缺少 DEEPSEEK_API_KEY，已停止，未发送请求")
    raise SystemExit

url = "https://cloud.vtrix.ai/llm/chat/completions"
model = "deepseek-v4.1-flash"
system_prompt = "你是游戏反馈分类器。只输出一个词：充值、性能、登录、社交、其它。"

feedbacks = [
    ("充了 68 元月卡，半小时了还没到账。", "充值"),
    ("进图就卡，掉到 10 帧，没法打。", "性能"),
    ("登录一直转圈，进不去游戏。", "登录"),
    ("公会聊天刷屏，根本看不清消息。", "社交"),
    ("今天天气不错，随便看看。", "其它"),
    ("月卡扣了两次钱，只到账一次。", "充值"),
    ("更新后一进主城就闪退。", "性能"),
    ("好友列表打不开，只能看不能点。", "社交"),
    ("登录界面黑屏，角色选不了。", "登录"),
    ("这活动页面挺好看的。", "其它"),
]

def classify_one(feedback):
    row = {
        "feedback": feedback,
        "status_code": None,
        "output": "",
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "elapsed_seconds": None,
        "error": "",
    }
    try:
        response = requests.post(
            url,
            headers={"Authorization": f"Bearer {key}"},
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
        row["status_code"] = response.status_code
        row["elapsed_seconds"] = round(response.elapsed.total_seconds(), 3)
        if response.status_code == 200:
            data = response.json()
            row["output"] = data["choices"][0]["message"]["content"].strip()
            usage = data.get("usage", {})
            row["prompt_tokens"] = usage.get("prompt_tokens") or 0
            row["completion_tokens"] = usage.get("completion_tokens") or 0
        else:
            row["error"] = "http_status"
    except requests.exceptions.Timeout:
        row["error"] = "timeout"
    except requests.exceptions.RequestException as error:
        row["error"] = type(error).__name__
    return row

rows = []
for feedback, expected in feedbacks:
    row = classify_one(feedback)
    row["expected"] = expected
    row["correct"] = row["output"] == expected
    rows.append(row)
    print(len(rows), row["status_code"], row["output"], row["error"])

table = pd.DataFrame(rows)
out_path = output_dir / "day65_batch.csv"
table.to_csv(out_path, index=False, encoding="utf-8-sig")

success_count = (table["status_code"] == 200).sum()
print("请求次数：", len(table))
print("成功次数：", int(success_count))
print("分类答对：", int(table["correct"].sum()))
print("输入 Token 合计：", int(table["prompt_tokens"].sum()))
print("输出 Token 合计：", int(table["completion_tokens"].sum()))
print("已导出：", out_path)