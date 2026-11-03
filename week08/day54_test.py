# Day 54 测验：使用 JOIN 多表关联与 GROUP BY 分组，找出成本最高的用户及按渠道统计 AI 成本

# 导入 sqlite3 数据库模块和 Path 路径工具
import sqlite3
from pathlib import Path

# 定位当前目录并连接 ai_monitor.db 数据库文件
project_dir = Path(__file__).parent
db_path = project_dir / "ai_monitor.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 查询 A（找成本最高用户）：
# JOIN users AS u ON c.user_id = u.user_id：通过共同的关联键 user_id 把调用表 c 和用户表 u 连起来
# GROUP BY 按用户分组，ORDER BY total_cost DESC 按总成本从高到低排序，LIMIT 1 只取第 1 名
top_user_sql = """
SELECT
    u.user_id,
    u.user_name,
    u.channel,
    COUNT(*) AS call_count,
    ROUND(SUM(c.cost), 2) AS total_cost
FROM api_calls AS c
JOIN users AS u ON c.user_id = u.user_id
GROUP BY u.user_id, u.user_name, u.channel
ORDER BY total_cost DESC
LIMIT 1;
"""
cursor.execute(top_user_sql)
top_user = cursor.fetchone()

print("=== 查询 A：成本最高的用户 ===")
print(
    f"成本最高的用户是 {top_user[1]}（{top_user[0]}），"
    f"来自 {top_user[2]} 渠道，共调用 {top_user[3]} 次，累计成本 {top_user[4]:.2f} 元。"
)

# 查询 B（按渠道统计 AI 成本）：
# 关联两张表后，按用户表里的来源渠道 u.channel 分组，统计每个渠道的调用次数和总成本
channel_cost_sql = """
SELECT
    u.channel,
    COUNT(*) AS call_count,
    ROUND(SUM(c.cost), 2) AS total_cost
FROM api_calls AS c
JOIN users AS u ON c.user_id = u.user_id
GROUP BY u.channel
ORDER BY total_cost DESC;
"""
cursor.execute(channel_cost_sql)
channel_rows = cursor.fetchall()

print("\n=== 查询 B：按渠道统计 AI 调用次数与总成本 ===")
for row in channel_rows:
    print(f"渠道：{row[0]} | 调用次数：{row[1]} 次 | 总成本：{row[2]:.2f} 元")

# 关闭数据库连接
conn.close()
