# Day 59 测验：为 3 条玩家反馈手写标准 JSON，并用 validate_output 校验后导出 CSV

import json
from pathlib import Path

import pandas as pd

from day59_json_schema import validate_output

project_dir = Path(__file__).parent
output_dir = project_dir / "output"
output_dir.mkdir(exist_ok=True)

labeled_cases = [
    {
        "feedback": "充了 68 元月卡，半小时了还没到账，很着急。",
        "label": {
            "category": "充值",
            "emotion": "焦虑",
            "priority": "高",
            "need_human": True,
            "reason": "充值未到账",
        },
    },
    {
        "feedback": "进图就卡，打副本掉到 10 帧，根本没法玩。",
        "label": {
            "category": "性能",
            "emotion": "愤怒",
            "priority": "高",
            "need_human": True,
            "reason": "反复卡顿",
        },
    },
    {
        "feedback": "今天天气不错，随便看看。",
        "label": {
            "category": "其它",
            "emotion": "中性",
            "priority": "低",
            "need_human": False,
            "reason": "与游戏问题无关",
        },
    },
]

rows = []
for item in labeled_cases:
    json_text = json.dumps(item["label"], ensure_ascii=False)
    result = validate_output(json_text)
    rows.append({
        "feedback": item["feedback"],
        "json_text": json_text,
        "ok": result["ok"],
        "error": result["error"],
    })

table = pd.DataFrame(rows)
csv_path = output_dir / "day59_labels.csv"
table.to_csv(csv_path, index=False, encoding="utf-8-sig")

print("已导出：", csv_path)
print(table.to_string(index=False))
