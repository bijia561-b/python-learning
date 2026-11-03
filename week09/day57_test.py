# Day 57 测验：为 4 个游戏 / AI 业务场景配置合适的 temperature，并导出为 CSV 配置表

import pandas as pd
from pathlib import Path

# 1. 定位当前目录与 output 输出文件夹
project_dir = Path(__file__).parent
output_dir = project_dir / "output"
output_dir.mkdir(exist_ok=True)

# 2. 为 4 个业务场景配置最合适的 temperature（从 0.0、0.3、0.8 中选择）
# 必含字段：scene, temperature, reason, risk_if_wrong
scene_configs = [
    {
        "scene": "玩家反馈自动打标签（只允许输出 JSON 格式分类）",
        "temperature": 0.0,
        "reason": "结构化分类与 JSON 提取要求 100% 稳定一致，零随机性",
        "risk_if_wrong": "温度过高会导致每次分类结果飘忽不定，甚至输出多余文字破坏 JSON 格式导致解析报错",
    },
    {
        "scene": "游戏充值/退款规则客服问答（严禁编造补偿金额）",
        "temperature": 0.0,
        "reason": "涉及金钱与规则红线，必须严格依据标准话术确定性回答",
        "risk_if_wrong": "温度过高容易产生幻觉（如乱承诺秒到账或赠送 8888 钻石），引发客诉与资损",
    },
    {
        "scene": "游戏节日活动宣传口号头脑风暴（需要提供 10 个不同创意）",
        "temperature": 0.8,
        "reason": "营销创意需要高多样性与发散思维，避免 10 条口号千篇一律",
        "risk_if_wrong": "温度过低会导致生成的口号高度重复、死板乏味，缺乏创意灵感",
    },
    {
        "scene": "每周运营数据日报文字润色（基于固定数字微调语气）",
        "temperature": 0.3,
        "reason": "在保证核心数据不跑偏的前提下，让行文语气比 0.0 更自然流畅",
        "risk_if_wrong": "温度过高可能篡改日报里的关键指标数字或夸大结论；0.0 则略显生硬机械",
    },
]

# 3. 转换为 DataFrame 并导出到 week09/output/day57_scene_config.csv
config_df = pd.DataFrame(scene_configs)
csv_path = output_dir / "day57_scene_config.csv"
config_df.to_csv(csv_path, index=False, encoding="utf-8-sig")

print("已导出场景温度配置表：", csv_path)
print("\n=== 4 个业务场景温度配置表 ===")
print(config_df.to_string(index=False))
