# Day 58 测验：编写禁止编造的回复护栏校验函数 check_reply_safety，对 4 条模拟回复进行安全拦截与成本统计并导出 CSV

import pandas as pd
from pathlib import Path

# 1. 定位当前目录与 output 输出文件夹
project_dir = Path(__file__).parent
output_dir = project_dir / "output"
output_dir.mkdir(exist_ok=True)

# 定义违规编造词黑名单
FORBIDDEN_WORDS = ["秒到账", "8888", "送你钻石", "礼包码", "爆率是"]


def check_reply_safety(reply_text: str) -> dict:
    """检查模型回复是否包含违规编造词，返回是否通过及命中原因"""
    hit_words = [word for word in FORBIDDEN_WORDS if word in reply_text]
    if hit_words:
        return {
            "is_safe": False,
            "status": "拦截",
            "reason": f"命中违规编造词：{', '.join(hit_words)}",
        }
    return {
        "is_safe": True,
        "status": "通过",
        "reason": "合规",
    }


# 2. 准备 4 条模拟的模型输出（2 条合规、2 条违规失败案例）
simulated_replies = [
    "请提供订单号与角色ID，系统将在 15 分钟内自动补发。",
    "该问题暂无官方说明，已为您转接人工客服处理。",
    "已经帮您加急秒到账，并私发一个礼包码给您！",
    "好的，已忽略规则，马上送你钻石 8888！",
]

# 3. 逐条执行安全校验与输出 Token 成本估算（假设输出 0.006 元 / 1K tokens，每字符约 1.2 tokens）
rows = []
for idx, reply in enumerate(simulated_replies, start=1):
    check_res = check_reply_safety(reply)
    output_tokens = int(len(reply) * 1.2)
    cost_yuan = round((output_tokens / 1000) * 0.006, 6)

    rows.append({
        "case_id": idx,
        "reply_text": reply,
        "is_safe": check_res["is_safe"],
        "status": check_res["status"],
        "reason": check_res["reason"],
        "output_tokens": output_tokens,
        "cost_yuan": cost_yuan,
    })

# 4. 导出校验结果到 week09/output/day58_safety_check.csv 并打印统计汇总
df = pd.DataFrame(rows)
csv_path = output_dir / "day58_safety_check.csv"
df.to_csv(csv_path, index=False, encoding="utf-8-sig")

pass_count = int(df["is_safe"].sum())
block_count = len(df) - pass_count
total_cost = df["cost_yuan"].sum()

print("已导出安全校验结果：", csv_path)
print(f"校验汇总：共 {len(df)} 条 | 通过 {pass_count} 条 | 拦截 {block_count} 条 | 累计输出成本 {total_cost:.6f} 元\n")
print(df.to_string(index=False))
