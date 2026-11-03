import sqlite3
from pathlib import Path

project_dir = Path(__file__).parent
db_path = project_dir / "ai_monitor.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 统计全局核心指标：总次数、成功次数、成功率(%)、平均耗时(ms)、总成本(元)
summary_sql = """
SELECT
    COUNT(*) AS total_calls,
    SUM(is_success) AS success_calls,
    ROUND(AVG(is_success) * 100, 1) AS success_rate_pct,
    ROUND(AVG(latency_ms), 1) AS avg_latency_ms,
    ROUND(SUM(cost), 2) AS total_cost
FROM api_calls;
"""

cursor.execute(summary_sql)
row = cursor.fetchone()

print("=== 全局 AI 调用指标 ===")
print(f"总调用次数：{row[0]}")
print(f"成功次数：  {row[1]}")
print(f"成功率：    {row[2]}%")
print(f"平均耗时：  {row[3]} ms")
print(f"总成本：    {row[4]} 元")

conn.close()