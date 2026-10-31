import sqlite3
from pathlib import Path

project_dir = Path(__file__).parent
db_path = project_dir / "ai_monitor.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 先清空表里的旧数据，保证脚本重复运行时不会重复塞入双倍数据
cursor.execute("DELETE FROM api_calls;")

# 准备 8 条模拟的 AI 功能调用记录
# 字段顺序：(user_id, feature, status_code, is_success, latency_ms, cost, created_at)
sample_calls = [
    ("u01", "ai_客服", 200, 1, 420.5, 0.02, "2026-10-30 10:01:00"),
    ("u02", "ai_翻译", 200, 1, 180.0, 0.01, "2026-10-30 10:05:00"),
    ("u01", "ai_总结", 500, 0, 1520.0, 0.00, "2026-10-30 10:12:00"),
    ("u03", "ai_客服", 200, 1, 510.2, 0.02, "2026-10-30 11:00:00"),
    ("u02", "ai_客服", 429, 0, 95.0, 0.00, "2026-10-31 09:15:00"),
    ("u01", "ai_客服", 200, 1, 390.8, 0.02, "2026-10-31 09:30:00"),
    ("u04", "ai_翻译", 200, 1, 210.4, 0.01, "2026-10-31 10:00:00"),
    ("u03", "ai_总结", 200, 1, 880.0, 0.05, "2026-10-31 10:20:00"),
]

insert_sql = """
INSERT INTO api_calls (user_id, feature, status_code, is_success, latency_ms, cost, created_at)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""

# 批量写入 8 条数据，并 commit 提交保存
cursor.executemany(insert_sql, sample_calls)
conn.commit()

# 查询1：SELECT * 表示查询所有字段
cursor.execute("SELECT * FROM api_calls;")
all_rows = cursor.fetchall()
print("总记录条数：", len(all_rows))
print("前 2 条完整记录：")
for row in all_rows[:2]:
    print(row)

# 查询2：只查询指定字段（user_id, feature, cost）
cursor.execute("SELECT user_id, feature, cost FROM api_calls;")
part_rows = cursor.fetchall()
print("\n只看用户、功能和成本：")
for row in part_rows:
    print(row)

conn.close()