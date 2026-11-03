import sqlite3
from pathlib import Path

project_dir = Path(__file__).parent
db_path = project_dir / "ai_monitor.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. 明细关联：查看每次调用对应的用户名、渠道、功能和成本
detail_sql = """
SELECT
    c.id,
    u.user_id,
    u.user_name,
    u.channel,
    c.feature,
    c.cost
FROM api_calls AS c
JOIN users AS u ON c.user_id = u.user_id
ORDER BY c.id;
"""
cursor.execute(detail_sql)
print("=== 调用明细（含用户名与渠道）===")
for row in cursor.fetchall():
    print(row)

# 2. 按用户分组统计：每个用户的调用次数、总成本，按总成本从高到低排序
user_cost_sql = """
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
ORDER BY total_cost DESC;
"""
cursor.execute(user_cost_sql)
print("\n=== 各用户调用次数与总成本排行 ===")
for row in cursor.fetchall():
    print(row)

conn.close()