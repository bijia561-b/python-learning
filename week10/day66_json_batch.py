import json
import os
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

project_dir = Path(__file__).parent
output_dir = project_dir / "output"
output_dir.mkdir(exist_ok=True)
load_dotenv(project_dir / ".env")

ALLOWED = {
    "category": ["性能", "充值", "登录", "社交", "其它"],
    "emotion": ["愤怒", "焦虑", "中性"],
    "priority": ["高", "中", "低"],
}

def extract_json_text(raw_text):
    text = raw_text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[1:-1]
        else:
            lines = lines[1:]
        text = "\n".join(lines).strip()
    return text

def validate_output(raw_text):
    try:
        data = json.loads(extract_json_text(raw_text))
    except json.JSONDecodeError:
        return {"ok": False, "error": "不是合法 JSON", "data": None}
    if not isinstance(data, dict):
        return {"ok": False, "error": "顶层不是对象", "data": None}
    for key in ["category", "emotion", "priority", "need_human", "reason"]:
        if key not in data:
            return {"ok": False, "error": f"缺少字段 {key}", "data": None}
    for key, choices in ALLOWED.items():
        if data[key] not in choices:
            return {"ok": False, "error": f"{key} 不在允许值内", "data": None}
    if not isinstance(data["need_human"], bool):
        return {"ok": False, "error": "need_human 不是布尔值", "data": None}
    if not isinstance(data["reason"], str) or len(data["reason"]) > 30:
        return {"ok": False, "error": "reason 不是短字符串", "data": None}
    return {"ok": True, "error": "", "data": data}

local_samples = [
    '{"category":"充值","emotion":"焦虑","priority":"高","need_human":true,"reason":"充值未到账"}',
    '```json\n{"category":"性能","emotion":"愤怒","priority":"高","need_human":true,"reason":"反复卡顿"}\n```',
    '{"category":"登录","emotion":"焦虑","priority":"高","reason":"进不去"}',
    '{"category":"卡顿","emotion":"愤怒","priority":"高","need_human":"是","reason":"太卡了"}',
]

print("本地校验：")
for text in local_samples:
    result = validate_output(text)
    print(result["ok"], result["error"])

key = os.getenv("DEEPSEEK_API_KEY")
if not key:
    print("缺少 DEEPSEEK_API_KEY，跳过真实请求")
    raise SystemExit

url = "https://cloud.vtrix.ai/llm/chat/completions"
model = "deepseek-v4.1-flash"
system_prompt = """你是游戏反馈分类器。只输出一个 JSON 对象，不要 Markdown，不要解释。
字段：
- category: 性能、充值、登录、社交、其它
- emotion: 愤怒、焦虑、中性
- priority: 高、中、低
- need_human: true 或 false
- reason: 不超过 30 字
充值未到账、无法登录、反复卡顿时 need_human 为 true。"""

feedbacks = [
    "充了 68 元月卡，半小时了还没到账。",
    "进图就卡，掉到 10 帧，没法打。",
    "今天天气不错，随便看看。",
]

rows = []
for feedback in feedbacks:
    row = {"feedback": feedback, "status_code": None, "raw_output": "", "ok": False, "error": "", "category": ""}
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
        if response.status_code != 200:
            row["error"] = "http_status"
        else:
            raw_output = response.json()["choices"][0]["message"]["content"]
            row["raw_output"] = raw_output
            checked = validate_output(raw_output)
            row["ok"] = checked["ok"]
            row["error"] = checked["error"]
            if checked["data"]:
                row["category"] = checked["data"]["category"]
    except requests.exceptions.Timeout:
        row["error"] = "timeout"
    except requests.exceptions.RequestException as error:
        row["error"] = type(error).__name__
    rows.append(row)
    print(row["status_code"], row["ok"], row["category"], row["error"])

out_path = output_dir / "day66_json_batch.csv"
pd.DataFrame(rows).to_csv(out_path, index=False, encoding="utf-8-sig")
print("已导出：", out_path)