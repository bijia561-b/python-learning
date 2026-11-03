import random
from pathlib import Path

# 固定随机种子，方便复现对比
random.seed(42)

def estimate_tokens_and_cost(prompt_text: str, output_text: str, max_context: int = 4096):
    """估算中英文混合文本的 Token 数、成本，并检查是否超出上下文窗口"""
    # 简易估算规则：每个字符约按 1.2 Token 计（中文偏多时的工程粗略估算）
    input_tokens = int(len(prompt_text) * 1.2)
    output_tokens = int(len(output_text) * 1.2)
    total_tokens = input_tokens + output_tokens

    # 假设某模型定价：输入 0.002 元 / 1K tokens，输出 0.006 元 / 1K tokens
    cost = (input_tokens / 1000) * 0.002 + (output_tokens / 1000) * 0.006
    is_overflow = total_tokens > max_context

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "cost_yuan": round(cost, 6),
        "is_overflow": is_overflow,
    }

# 模拟候选回复及其原始得分（概率权重）
candidates = [
    ("【标准回复】您的退款申请已提交，预计 1-3 个工作日原路退回。", 0.75),
    ("【温和回复】别着急呀，退款已经在处理中啦，大概 1-3 天就会回到您的账户~", 0.20),
    ("【发散/幻觉回复】退款已秒到账，另外赠送您 8888 钻石作为补偿！", 0.05),
]

def sample_by_temperature(temperature: float, runs: int = 5):
    """模拟不同温度下的多次输出表现"""
    results = []
    for _ in range(runs):
        if temperature == 0.0:
            # 温度为 0：贪婪解码，永远选概率最高的第 1 个
            chosen = candidates[0][0]
        else:
            # 温度越高，权重差距被拉平，低概率的发散/幻觉候选项越容易被抽中
            weights = [prob ** (1.0 / temperature) for _, prob in candidates]
            chosen = random.choices([text for text, _ in candidates], weights=weights, k=1)[0]
        results.append(chosen)
    return results

print("=== 1. 不同温度下的 5 次输出对比 ===")
for temp in [0.0, 0.7, 1.5]:
    print(f"\n【temperature = {temp}】")
    for idx, reply in enumerate(sample_by_temperature(temp), start=1):
        print(f"  第{idx}次: {reply}")

print("\n=== 2. Token 与上下文窗口检查 ===")
short_prompt = "玩家反馈：充值 68 元未到账，请帮我查询并回复处理时效。"
normal_reply = candidates[0][0]
print("正常请求：", estimate_tokens_and_cost(short_prompt, normal_reply, max_context=200))

# 模拟一条塞了过长历史记录的超限请求（失败案例）
long_prompt = short_prompt * 20
print("超长请求：", estimate_tokens_and_cost(long_prompt, normal_reply, max_context=200))