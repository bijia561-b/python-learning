# Day 53 测验：使用 GROUP BY feature 按每个 AI 功能分组统计调用次数、成功率、平均耗时与总成本

# 导入 sqlite3 数据库模块和 Path 路径工具
import sqlite3
from pathlib import Path

# 定位当前目录并连接 ai_monitor.db 数据库文件
project_dir = Path(__file__).parent
db_path = project_dir / "ai_monitor.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 编写按功能分组（GROUP BY feature）的聚合统计 SQL：
# COUNT(*)：统计该功能被调用了多少次
# ROUND(AVG(is_success) * 100, 1)：计算该功能的成功率百分比，并四舍五入保留 1 位小数
# ROUND(AVG(latency_ms), 1)：计算该功能的平均耗时（毫秒），保留 1 位小数
# ROUND(SUM(cost), 2)：计算该功能的累计总成本（元），保留 2 位小数
# ORDER BY COUNT(*) DESC：按调用次数从高到低排序
feature_sql = """
SELECT
    feature,
    COUNT(*) AS call_count,
    ROUND(AVG(is_success) * 100, 1) AS success_rate_pct,
    ROUND(AVG(latency_ms), 1) AS avg_latency_ms,
    ROUND(SUM(cost), 2) AS total_cost
FROM api_calls
GROUP BY feature
ORDER BY COUNT(*) DESC;
"""

# 执行查询并取回所有分组结果
cursor.execute(feature_sql)
rows = cursor.fetchall()

print("=== 按 AI 功能分组统计 ===")
for row in rows:
    print(
        f"功能：{row[0]} | 调用次数：{row[1]} | "
        f"成功率：{row[2]}% | 平均耗时：{row[3]} ms | 总成本：{row[4]} 元"
    )

# 关闭数据库连接
conn.close()
