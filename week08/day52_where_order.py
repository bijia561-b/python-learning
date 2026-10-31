import sqlite3
from pathlib import Path

project_dir = Path(__file__).parent
db_path = project_dir / "ai_monitor.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. 查询所有失败的调用（is_success = 0）
failed_sql = """
SELECT id, user_id, feature, status_code, latency_ms, created_at
FROM api_calls
WHERE is_success = 0;
"""
cursor.execute(failed_sql)
print("失败请求列表：")
for row in cursor.fetchall():
    print(row)

# 2. 查询慢请求（耗时 > 500 毫秒），并按耗时从高到低排序
slow_sql = """
SELECT id, user_id, feature, status_code, latency_ms
FROM api_calls
WHERE latency_ms > 500
ORDER BY latency_ms DESC;
"""
cursor.execute(slow_sql)
print("\n慢请求（> 500ms，从慢到快）：")
for row in cursor.fetchall():
    print(row)

conn.close()