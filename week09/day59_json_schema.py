import json
from pathlib import Path

project_dir = Path(__file__).parent
output_dir = project_dir / "output"
output_dir.mkdir(exist_ok=True)

ALLOWED = {
    "category": ["性能", "充值", "登录", "社交", "其它"],
    "emotion": ["愤怒", "焦虑", "中性"],
    "priority": ["高", "中", "低"],
}

SYSTEM_PROMPT = """你是游戏反馈分类器。只输出一个 JSON 对象，不要 Markdown，不要解释。
字段：
- category: 字符串，只能是 性能、充值、登录、社交、其它
- emotion: 字符串，只能是 愤怒、焦虑、中性
- priority: 字符串，只能是 高、中、低
- need_human: 布尔值 true 或 false
- reason: 字符串，不超过 30 字
充值未到账、无法登录、反复卡顿时 need_human 为 true。
"""

def validate_output(raw_text: str) -> dict:
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        return {"ok": False, "error": "不是合法 JSON"}

    if not isinstance(data, dict):
        return {"ok": False, "error": "顶层不是对象"}

    required = ["category", "emotion", "priority", "need_human", "reason"]
    for key in required:
        if key not in data:
            return {"ok": False, "error": f"缺少字段 {key}"}

    for key, choices in ALLOWED.items():
        if data[key] not in choices:
            return {"ok": False, "error": f"{key} 不在允许值内"}

    if not isinstance(data["need_human"], bool):
        return {"ok": False, "error": "need_human 不是布尔值"}

    if not isinstance(data["reason"], str) or len(data["reason"]) > 30:
        return {"ok": False, "error": "reason 不是短字符串"}

    return {"ok": True, "error": "", "data": data}

if __name__ == "__main__":
    samples = [
        '{"category":"充值","emotion":"焦虑","priority":"高","need_human":true,"reason":"充值未到账"}',
        '分类结果如下：{"category":"性能","emotion":"愤怒","priority":"高","need_human":true,"reason":"反复卡顿"}',
        '{"category":"卡顿","emotion":"愤怒","priority":"高","need_human":"是","reason":"太卡了"}',
    ]

    for text in samples:
        print(validate_output(text))

    (output_dir / "day59_system_prompt.txt").write_text(SYSTEM_PROMPT, encoding="utf-8")