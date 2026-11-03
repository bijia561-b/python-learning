import sqlite3
import pandas as pd
from pathlib import Path

project_dir = Path(__file__).parent
db_path = project_dir / "ai_monitor.db"
output_dir = project_dir / "output"
output_dir.mkdir(exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. 查询全局汇总指标
summary_sql = """
SELECT
    COUNT(*) AS total_calls,
    SUM(is_success) AS success_calls,
    ROUND(AVG(is_success) * 100, 1) AS success_rate_pct,
    ROUND(AVG(latency_ms), 1) AS avg_latency_ms,
    ROUND(SUM(cost), 2) AS total_cost
FROM api_calls;
"""
total_calls, success_calls, success_rate, avg_latency, total_cost = cursor.execute(summary_sql).fetchone()

# 2. 用 Pandas 直接把按功能统计的 SQL 读成 DataFrame，并导出 CSV
feature_sql = """
SELECT
    feature AS 功能名称,
    COUNT(*) AS 调用次数,
    ROUND(AVG(is_success) * 100, 1) AS 成功率百分比,
    ROUND(AVG(latency_ms), 1) AS 平均耗时毫秒,
    ROUND(SUM(cost), 2) AS 总成本元
FROM api_calls
GROUP BY feature
ORDER BY 调用次数 DESC;
"""
feature_df = pd.read_sql_query(feature_sql, conn)
csv_path = output_dir / "day55_feature_report.csv"
feature_df.to_csv(csv_path, index=False, encoding="utf-8-sig")

# 3. 找出最慢请求与成本最高用户（用于写进日报结论）
slowest = cursor.execute("""
    SELECT user_id, feature, status_code, latency_ms
    FROM api_calls
    ORDER BY latency_ms DESC
    LIMIT 1;
""").fetchone()

top_user = cursor.execute("""
    SELECT u.user_name, u.channel, ROUND(SUM(c.cost), 2) AS total_cost
    FROM api_calls AS c
    JOIN users AS u ON c.user_id = u.user_id
    GROUP BY u.user_id, u.user_name, u.channel
    ORDER BY total_cost DESC
    LIMIT 1;
""").fetchone()

conn.close()

# 4. 生成并导出 Markdown 日报
md_content = f"""# AI 功能调用监控日报

## 1. 全局概览
- 总调用次数：{total_calls} 次（成功 {success_calls} 次，成功率 {success_rate}%）
- 平均耗时：{avg_latency} ms
- 累计总成本：{total_cost:.2f} 元

## 2. 重点关注与异常
- 最慢请求：用户 `{slowest[0]}` 调用 `{slowest[1]}`，状态码 {slowest[2]}，耗时 {slowest[3]} ms
- 成本最高用户：{top_user[0]}（来源：{top_user[1]}），累计成本 {top_user[2]:.2f} 元
"""

md_path = output_dir / "day55_daily_report.md"
md_path.write_text(md_content, encoding="utf-8")

print("已导出 CSV：", csv_path)
print("已导出日报：", md_path)
print("\n=== 功能统计表 ===")
print(feature_df.to_string(index=False))