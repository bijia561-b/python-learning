# Day 55 测验：使用 SUBSTR 截取日期、pd.read_sql_query 读取每日趋势表并导出为 CSV

# 导入 sqlite3 数据库模块、pandas 数据处理库与 Path 路径工具
import sqlite3
import pandas as pd
from pathlib import Path

# 定位当前目录、数据库文件与 output 输出文件夹
project_dir = Path(__file__).parent
db_path = project_dir / "ai_monitor.db"
output_dir = project_dir / "output"
output_dir.mkdir(exist_ok=True)

# 1. 连接 SQLite 数据库
conn = sqlite3.connect(db_path)

# 2. 编写按天汇总的 SQL 查询：
# SUBSTR(created_at, 1, 10)：从第 1 个字符开始截取 10 个字符（如把 '2026-10-30 10:01:00' 截取成 '2026-10-30'）
# 按截取出来的日期 call_date 分组（GROUP BY），统计每天的调用次数、成功率和当日总成本
daily_sql = """
SELECT
    SUBSTR(created_at, 1, 10) AS call_date,
    COUNT(*) AS call_count,
    ROUND(AVG(is_success) * 100, 1) AS success_rate_pct,
    ROUND(SUM(cost), 2) AS daily_cost
FROM api_calls
GROUP BY call_date
ORDER BY call_date;
"""

# 3. 用 pd.read_sql_query(SQL语句, 数据库连接) 一步执行 SQL 并把查询结果直接转成 Pandas 的 DataFrame 表格
daily_df = pd.read_sql_query(daily_sql, conn)

# 关闭数据库连接
conn.close()

# 4. 将每日趋势表格导出到 week08/output/day55_daily_trend.csv（不带行号索引，使用 utf-8-sig 防止 Excel 中文乱码）
csv_path = output_dir / "day55_daily_trend.csv"
daily_df.to_csv(csv_path, index=False, encoding="utf-8-sig")

print("已导出每日趋势 CSV：", csv_path)
print("\n=== 每日调用趋势表 ===")
print(daily_df.to_string(index=False))
