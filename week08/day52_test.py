# Day 52 测验：使用 ORDER BY + LIMIT 找出耗时最长的请求，并用 WHERE ... AND ... 多条件组合筛选

# 导入 sqlite3 数据库模块和 Path 路径工具
import sqlite3
from pathlib import Path

# 定位当前目录并连接 ai_monitor.db 数据库文件
project_dir = Path(__file__).parent
db_path = project_dir / "ai_monitor.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 查询 A（找耗时最长请求）：
# ORDER BY latency_ms DESC 表示按耗时从高到低（降序）排列
# LIMIT 1 表示只取排在最前面的第 1 条记录（也就是耗时最长的那一条）
slowest_sql = """
SELECT user_id, feature, status_code, latency_ms
FROM api_calls
ORDER BY latency_ms DESC
LIMIT 1;
"""
cursor.execute(slowest_sql)
# fetchone() 只取回 1 条结果（也可以用 fetchall() 取列表）
slowest_row = cursor.fetchone()
print("查询 A —— 耗时最长的 1 条请求 (user_id, feature, status_code, latency_ms)：")
print(slowest_row)

# 查询 B（多条件组合）：
# WHERE is_success = 1 AND feature = 'ai_客服'：同时满足“调用成功”并且“功能是 ai_客服”（注意 SQL 判断相等用单个 =）
# ORDER BY latency_ms ASC：按耗时从低到高（升序，最快到最慢）排列
cs_success_sql = """
SELECT user_id, feature, status_code, latency_ms, cost, created_at
FROM api_calls
WHERE is_success = 1 AND feature = 'ai_客服'
ORDER BY latency_ms ASC;
"""
cursor.execute(cs_success_sql)
cs_rows = cursor.fetchall()
print("\n查询 B —— 成功的 'ai_客服' 调用（按耗时从低到高 ASC）：")
for row in cs_rows:
    print(row)

# 关闭数据库连接
conn.close()
