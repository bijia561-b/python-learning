import json
from pathlib import Path

project_dir = Path(__file__).parent
output_dir = project_dir / "output"
output_dir.mkdir(exist_ok=True)

SYSTEM_PROMPT = """你是游戏反馈分类器。只输出一个 JSON 对象，不要 Markdown，不要解释。
字段允许值：
- category: 性能、充值、登录、社交、其它
- emotion: 愤怒、焦虑、中性
- priority: 高、中、低
- need_human: true 或 false
- reason: 不超过 30 字的字符串
充值未到账、无法登录、反复卡顿时 need_human 为 true。
"""

USER_TEMPLATE = """玩家反馈：{feedback}
请按系统规则只输出一个 JSON 对象。"""

feedbacks = [
    "充了 68 元月卡，半小时了还没到账，很着急。",
    "进图就卡，打副本掉到 10 帧，根本没法玩。",
    "今天天气不错，随便看看。",
]

def build_prompt(feedback: str) -> dict:
    user_prompt = USER_TEMPLATE.format(feedback=feedback)
    total_chars = len(SYSTEM_PROMPT) + len(user_prompt)
    return {
        "feedback": feedback,
        "temperature": 0,
        "system_prompt": SYSTEM_PROMPT,
        "user_prompt": user_prompt,
        "est_input_tokens": int(total_chars * 1.2),
    }

prompts = [build_prompt(text) for text in feedbacks]
for item in prompts:
    print(item["est_input_tokens"], item["user_prompt"].splitlines()[0])

out_path = output_dir / "day60_prompts.json"
out_path.write_text(json.dumps(prompts, ensure_ascii=False, indent=2), encoding="utf-8")
print("已导出：", out_path)