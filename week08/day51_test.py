# Day 51 测验：向 users 表批量插入用户数据（INSERT），并查询所有用户及 u01（小林）的调用记录（SELECT）

# 导入 sqlite3 数据库模块和 Path 路径工具
import sqlite3
from pathlib import Path

# 定位当前目录并连接同一个 ai_monitor.db 数据库文件
project_dir = Path(__file__).parent
db_path = project_dir / "ai_monitor.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. 先清空 users 表里的旧用户数据，保证重复运行脚本时不会报错或重复插入
cursor.execute("DELETE FROM users;")

# 2. 准备 4 位用户的列表数据，顺序对应：(user_id, user_name, vip_level, channel)
sample_users = [
    ("u01", "小林", 3, "抖音"),
    ("u02", "小周", 1, "微信"),
    ("u03", "小王", 5, "官网"),
    ("u04", "小陈", 2, "抖音"),
]

# 编写插入 SQL 语句，4 个问号 ? 是占位符，会依次填入上面每条元组的 4 个值
insert_users_sql = """
INSERT INTO users (user_id, user_name, vip_level, channel)
VALUES (?, ?, ?, ?);
"""

# 用 executemany 一次性批量插入 4 位用户，并调用 conn.commit() 提交保存到硬盘
cursor.executemany(insert_users_sql, sample_users)
conn.commit()

# 3. 查询 users 表中的所有用户（只看 user_id, user_name, channel 三个字段）
cursor.execute("SELECT user_id, user_name, channel FROM users;")
users_rows = cursor.fetchall()

print("所有用户列表（共", len(users_rows), "人）：")
for row in users_rows:
    print(row)

# 4. 查询 api_calls 表中 user_id 为 'u01'（小林）的所有调用记录
cursor.execute("SELECT user_id, feature, status_code FROM api_calls WHERE user_id = 'u01';")
u01_calls = cursor.fetchall()

print("\nu01（小林）的调用记录（共", len(u01_calls), "条）：")
for row in u01_calls:
    print(row)

# 5. 关闭数据库连接
conn.close()
