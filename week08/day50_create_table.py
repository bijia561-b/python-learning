# Day 50：使用 Python 内置的 sqlite3 创建数据库文件与 api_calls（AI 接口调用记录）表

# 导入 Python 自带的轻量级数据库模块 sqlite3（不需要 pip install）
import sqlite3
# 导入 Path，用来拼接当前脚本所在目录的文件路径
from pathlib import Path

# Path(__file__).parent 表示当前这个 .py 文件所在的文件夹（即 week08）
project_dir = Path(__file__).parent
# 指定数据库文件名为 ai_monitor.db（存放在 week08 目录下）
db_path = project_dir / "ai_monitor.db"

# 连接数据库：如果 ai_monitor.db 文件还不存在，sqlite3 会自动创建它
conn = sqlite3.connect(db_path)
# 创建“游标”（cursor），可以理解成数据库里的操作员，所有 SQL 命令都靠它去执行
cursor = conn.cursor()

# 编写建表 SQL 语句（用三引号 """...""" 可以写多行文本）：
# CREATE TABLE IF NOT EXISTS api_calls：如果还没有 api_calls 这张表就新建；已经有了就不报错跳过
# INTEGER 是整数，REAL 是小数，TEXT 是字符串文本；NOT NULL 表示该字段必填、不能为空
create_sql = """
CREATE TABLE IF NOT EXISTS api_calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- id：主键，每新增一条记录会自动按 1, 2, 3... 编号
    user_id TEXT NOT NULL,                 -- user_id：调用该功能的用户编号
    feature TEXT NOT NULL,                 -- feature：调用的 AI 功能名称（如客服、翻译）
    status_code INTEGER NOT NULL,          -- status_code：HTTP 状态码（如 200、429、500）
    is_success INTEGER NOT NULL,           -- is_success：是否成功（1 表示成功，0 表示失败）
    latency_ms REAL NOT NULL,              -- latency_ms：请求耗时（毫秒，允许有小数）
    cost REAL NOT NULL,                    -- cost：本次调用花费的成本（元，允许有小数）
    created_at TEXT NOT NULL               -- created_at：调用发生的时间字符串
);
"""

# 让游标执行上面写好的建表 SQL 语句
cursor.execute(create_sql)
# conn.commit() 表示“提交保存”，把建表操作真正写入到 .db 数据库文件中
conn.commit()

# PRAGMA table_info(表名) 是 SQLite 专用查询命令，用来查看这张表有哪些字段、是什么类型
cursor.execute("PRAGMA table_info(api_calls);")
# .fetchall() 把查询到的所有结果取出来，变成一个 Python 列表（每一行对应表里的一个字段信息）
columns = cursor.fetchall()

print("数据库文件：", db_path)
print("api_calls 字段列表：")
# 逐行打印每个字段的信息：(序号, 字段名, 类型, 是否必填, 默认值, 是否主键)
for col in columns:
    print(col)

# 用完数据库后关闭连接，释放文件占用
conn.close()
