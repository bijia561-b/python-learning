# Day 37 测验：绘制 DAU 趋势折线图，同时标出最高点与最低点并保存新图片

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

input_path="week06/day37_dau.csv"
output_path="week06/output/day37_dau_test.png"

table=pd.read_csv(input_path)
table["login_date"]=pd.to_datetime(table["login_date"]).dt.date

# 设置中文字体与负号显示
plt.rcParams["font.sans-serif"]=["Microsoft YaHei","SimHei"]
plt.rcParams["axes.unicode_minus"]=False

# 绘制基础折线图及标题、坐标轴名称
plt.plot(table["login_date"],table["dau"],marker="o")
plt.title("DAU-TREND")
plt.xlabel("date")
plt.ylabel("dau")
plt.xticks(rotation=30)
plt.tight_layout()

# 分别找出 DAU 最低和最高的日期与数值
lowest_day=table.loc[table["dau"].idxmin(),"login_date"]
lowest_dau=table["dau"].min()
highest_day=table.loc[table["dau"].idxmax(),"login_date"]
highest_dau=table["dau"].max()

# 同时在最低点（粉色）和最高点（绿色）画高亮圆点
plt.scatter([lowest_day,highest_day],
            [lowest_dau,highest_dau],
            color=["pink","green"],
            zorder=5,
)

# 用循环给最低点和最高点分别加上文字标注
for day,dau,label,offset in [
    (lowest_day,lowest_dau,"最低",(5,10)),
    (highest_day,highest_dau,"最高",(5,-15))
]:
    plt.annotate(
        f"{label}{int(dau)}",
        xy=(day,dau),
        xytext=offset,
        textcoords="offset points",
)

# 保存图片到 output 目录
plt.savefig(output_path)
print("已保存",output_path)
print("DAU最高",highest_day,highest_dau)
