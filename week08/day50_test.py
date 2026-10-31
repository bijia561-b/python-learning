# Day 50 测验：在同一个 ai_monitor.db 数据库中创建 users（用户）表并查看表结构

# 导入 sqlite3 数据库模块和 Path 路径工具
import sqlite3
from pathlib import Path

# 定位当前脚本所在目录（week08），并指向同一个数据库文件 ai_monitor.db
project_dir = Path(__file__).parent
db_path = project_dir / "ai_monitor.db"

# 1. 打开数据库连接，并创建游标（办事员）cursor
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 2. 编写创建 users 用户表的 SQL 语句：
# user_id 作为 TEXT PRIMARY KEY（文本主键，唯一标识每个用户，不能重复）
create_users_sql = """
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,      -- user_id：用户唯一 ID（主键）
    user_name TEXT NOT NULL,       -- user_name：用户名称（必填）
    vip_level INTEGER NOT NULL,    -- vip_level：VIP 等级（整数，必填）
    channel TEXT NOT NULL          -- channel：来源渠道（文本，必填）
);
"""

# 3. 执行建表语句并 commit() 提交保存到数据库文件
cursor.execute(create_users_sql)
conn.commit()

# 4. 查询 users 表的字段结构并取出全部结果
cursor.execute("PRAGMA table_info(users);")
columns = cursor.fetchall()

print("数据库文件：", db_path)
print("users 表字段列表：")
for col in columns:
    print(col)

# 5. 关闭数据库连接
conn.close()
