# Day 60 测验：用带 player_id 和 feedback 两个占位符的模板生成 3 条 Prompt

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

USER_TEMPLATE = """玩家ID：{player_id}
玩家反馈：{feedback}
请按系统规则只输出一个 JSON 对象。"""

cases = [
    ("u01", "登录一直转圈，进不去游戏。"),
    ("u02", "公会聊天刷屏，根本看不清消息。"),
    ("u03", "这活动页面挺好看的。"),
]


def build_prompt(player_id: str, feedback: str) -> dict:
    user_prompt = USER_TEMPLATE.format(player_id=player_id, feedback=feedback)
    total_chars = len(SYSTEM_PROMPT) + len(user_prompt)
    return {
        "player_id": player_id,
        "feedback": feedback,
        "temperature": 0,
        "system_prompt": SYSTEM_PROMPT,
        "user_prompt": user_prompt,
        "est_input_tokens": int(total_chars * 1.2),
    }


prompts = [build_prompt(player_id, feedback) for player_id, feedback in cases]
for item in prompts:
    print(item["user_prompt"].splitlines()[0])

out_path = output_dir / "day60_three_prompts.json"
out_path.write_text(json.dumps(prompts, ensure_ascii=False, indent=2), encoding="utf-8")
print("已导出：", out_path)
