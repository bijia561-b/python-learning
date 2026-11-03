# Day 56 第 8 周项目（作品集项目 3）：AI 功能调用日志分析器
# 功能：读取 CSV 原始数据 -> 导入 SQLite 数据库 -> 执行多维 SQL 聚合分析 -> 导出 CSV 统计表与 Markdown 监控报告

import sqlite3
import pandas as pd
from pathlib import Path

# 1. 定位项目根目录、data 数据目录、output 输出目录与 SQLite 数据库路径
project_dir = Path(__file__).parent
data_dir = project_dir / "data"
output_dir = project_dir / "output"
output_dir.mkdir(exist_ok=True)
db_path = project_dir / "log_analyzer.db"

# 2. 连接数据库并创建游标（办事员）
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 3. 创建 users（用户表）和 api_calls（调用日志表）
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,      -- 用户唯一 ID（主键）
    user_name TEXT NOT NULL,       -- 用户名
    vip_level INTEGER NOT NULL,    -- VIP 等级
    channel TEXT NOT NULL          -- 来源渠道
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS api_calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 自增主键
    user_id TEXT NOT NULL,                 -- 调用用户 ID
    feature TEXT NOT NULL,                 -- AI 功能名称
    status_code INTEGER NOT NULL,          -- HTTP 状态码
    is_success INTEGER NOT NULL,           -- 是否成功（1 成功，0 失败）
    latency_ms REAL NOT NULL,              -- 耗时（毫秒）
    cost REAL NOT NULL,                    -- 调用成本（元）
    created_at TEXT NOT NULL               -- 调用时间
);
""")

# 先清空旧数据，保证脚本重复运行时数据不会翻倍
cursor.execute("DELETE FROM users;")
cursor.execute("DELETE FROM api_calls;")

# 4. 读取 CSV 文件并用 executemany 批量写入 SQLite 数据库
users_df = pd.read_csv(data_dir / "users.csv")
calls_df = pd.read_csv(data_dir / "api_calls.csv")

cursor.executemany(
    "INSERT INTO users (user_id, user_name, vip_level, channel) VALUES (?, ?, ?, ?);",
    users_df[["user_id", "user_name", "vip_level", "channel"]].itertuples(index=False, name=None),
)

cursor.executemany(
    """
    INSERT INTO api_calls (user_id, feature, status_code, is_success, latency_ms, cost, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """,
    calls_df[["user_id", "feature", "status_code", "is_success", "latency_ms", "cost", "created_at"]].itertuples(index=False, name=None),
)
conn.commit()

# 5. 核心 SQL 查询 1：全局概览指标（总调用次数、成功次数、失败次数、成功率、平均耗时、累计总成本）
summary_sql = """
SELECT
    COUNT(*) AS total_calls,
    SUM(is_success) AS success_calls,
    SUM(1 - is_success) AS fail_calls,
    ROUND(AVG(is_success) * 100, 1) AS success_rate_pct,
    ROUND(AVG(latency_ms), 1) AS avg_latency_ms,
    ROUND(SUM(cost), 2) AS total_cost
FROM api_calls;
"""
total_calls, success_calls, fail_calls, success_rate, avg_latency, total_cost = cursor.execute(summary_sql).fetchone()

# 6. 核心 SQL 查询 2：按功能汇总统计，并导出到 output/feature_summary.csv
# SUM(1 - is_success) 用于统计失败次数（失败时 1-0=1，成功时 1-1=0）
feature_sql = """
SELECT
    feature,
    COUNT(*) AS call_count,
    SUM(1 - is_success) AS fail_count,
    ROUND(AVG(is_success) * 100, 1) AS success_rate_pct,
    ROUND(AVG(latency_ms), 1) AS avg_latency_ms,
    ROUND(SUM(cost), 2) AS total_cost
FROM api_calls
GROUP BY feature
ORDER BY fail_count DESC, call_count DESC;
"""
feature_df = pd.read_sql_query(feature_sql, conn)
feature_csv_path = output_dir / "feature_summary.csv"
feature_df.to_csv(feature_csv_path, index=False, encoding="utf-8-sig")

# 7. 核心 SQL 查询 3：找出失败次数最多的功能（按 fail_count DESC 排第 1 名）
most_failed_sql = """
SELECT
    feature,
    COUNT(*) AS call_count,
    SUM(1 - is_success) AS fail_count,
    ROUND(AVG(is_success) * 100, 1) AS success_rate_pct,
    ROUND(AVG(latency_ms), 1) AS avg_latency_ms
FROM api_calls
GROUP BY feature
ORDER BY fail_count DESC
LIMIT 1;
"""
worst_feature, worst_calls, worst_fails, worst_rate, worst_latency = cursor.execute(most_failed_sql).fetchone()

# 8. 核心 SQL 查询 4：关联 users 表按用户统计调用成本排行，并导出到 output/user_cost_rank.csv
user_rank_sql = """
SELECT
    u.user_id,
    u.user_name,
    u.vip_level,
    u.channel,
    COUNT(*) AS call_count,
    ROUND(SUM(c.cost), 2) AS total_cost
FROM api_calls AS c
JOIN users AS u ON c.user_id = u.user_id
GROUP BY u.user_id, u.user_name, u.vip_level, u.channel
ORDER BY total_cost DESC, call_count DESC;
"""
user_rank_df = pd.read_sql_query(user_rank_sql, conn)
user_csv_path = output_dir / "user_cost_rank.csv"
user_rank_df.to_csv(user_csv_path, index=False, encoding="utf-8-sig")

# 取出成本最高的用户（排第 1 行）与耗时最长的单次请求
top_user_row = cursor.execute(user_rank_sql).fetchone()
slowest_row = cursor.execute("""
SELECT c.user_id, u.user_name, c.feature, c.status_code, c.latency_ms, c.created_at
FROM api_calls AS c
JOIN users AS u ON c.user_id = u.user_id
ORDER BY c.latency_ms DESC
LIMIT 1;
""").fetchone()

conn.close()

# 9. 生成并导出 Markdown 监控分析报告 output/monitor_report.md
report_md = f"""# AI 功能调用监控分析报告

## 1. 全局概览
- 总调用次数：{total_calls} 次（成功 {success_calls} 次，失败 {fail_calls} 次）
- 总成功率：{success_rate}%
- 全局平均耗时：{avg_latency} ms
- 累计总成本：{total_cost:.2f} 元

## 2. 异常与风险定位
- **失败最多的功能**：`{worst_feature}`（共调用 {worst_calls} 次，失败 {worst_fails} 次，成功率仅 {worst_rate}%，平均耗时 {worst_latency} ms）
- **最慢单次请求**：用户 `{slowest_row[1]}（{slowest_row[0]}）` 在 `{slowest_row[5]}` 调用 `{slowest_row[2]}`，状态码 `{slowest_row[3]}`，耗时 `{slowest_row[4]} ms`
- **成本最高用户**：`{top_user_row[1]}（{top_user_row[0]}）`，来源渠道 `{top_user_row[3]}`，共调用 {top_user_row[4]} 次，累计成本 `{top_user_row[5]:.2f} 元`

## 3. 优化建议
- **优先排查 `{worst_feature}` 稳定性与超时风险**：该功能失败 {worst_fails} 次（含 500 服务端错误与 504 网关超时），平均耗时高达 {worst_latency} ms，建议设置分段总结/限制输入长度，并增加超时降级与有限重试。
- **关注 `ai_客服` 的 429 限流告警**：针对高频调用用户增加客户端请求节流与结果缓存。
- **高成本功能配额管理**：`{top_user_row[1]}`（{top_user_row[3]}渠道）因调用单价较高的 `ai_总结` 产生最高成本（{top_user_row[5]:.2f} 元），建议对高成本模型设置每日调用限额或分级路由。
"""

report_path = output_dir / "monitor_report.md"
report_path.write_text(report_md, encoding="utf-8")

print("数据库已生成：", db_path)
print("功能统计已导出：", feature_csv_path)
print("用户成本排行已导出：", user_csv_path)
print("监控报告已导出：", report_path)
print("\n=== 按功能汇总 ===")
print(feature_df.to_string(index=False))
print("\n=== 按用户成本排行 ===")
print(user_rank_df.to_string(index=False))
print("\n" + report_md)
