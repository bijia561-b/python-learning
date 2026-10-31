# Day 37：使用 matplotlib 绘制 DAU 趋势折线图，并在图上标记最低点

import pandas as pd
# 导入画图库 matplotlib.pyplot，简写为 plt
import matplotlib.pyplot as plt
from pathlib import Path

project_dir=Path(__file__).parent
table=pd.read_csv(project_dir/"day37_dau.csv")
table["login_date"]=pd.to_datetime(table["login_date"]).dt.date

print(table)

# 配置中文字体（微软雅黑 / 黑体），防止图表上的中文标题变成方框；axes.unicode_minus=False 保证负号正常显示
plt.rcParams["font.sans-serif"]=["Microsoft YaHei","SimHei"]
plt.rcParams["axes.unicode_minus"]=False

# plt.plot(横轴数据, 纵轴数据, marker="o") 画折线图，marker="o" 表示在每个数据点上画圆点
plt.plot(table["login_date"],table["dau"],marker="o")
plt.title("活动期间DAU趋势")
plt.xlabel("日期")
plt.ylabel("DAU")
# 把横轴日期文字倾斜 30 度，避免挤在一起重叠
plt.xticks(rotation=30)
# 自动调整边距，防止文字被裁切
plt.tight_layout()

# 找出 DAU 最低的那一行对应的日期（idxmin 找最小值的行号）和具体数值（min）
lowest_day=table.loc[table["dau"].idxmin(),"login_date"]
lowest_dau=table["dau"].min()

# plt.scatter 在最低点位置单独画一个红色圆点（zorder=5 让红点盖在折线上面）
plt.scatter([lowest_day],[lowest_dau],color="red",zorder=5)
# plt.annotate 在最低点旁边写上“最低90”的文字说明，xytext=(10,15) 表示文字往右偏 10、往上偏 15 个像素点
plt.annotate(
    f"最低{int(lowest_dau)}",
    xy=(lowest_day,lowest_dau),
    xytext=(10,15),
    textcoords="offset points",
)

# 将画好的图保存为 PNG 图片文件
output_dir=project_dir/"output"
output_dir.mkdir(exist_ok=True)
output_path=output_dir/"day37_dau_trend.png"
plt.savefig(output_path)
print("已保存：",output_path)

print("dau最低日期:",lowest_day)
print("dau最低值:",lowest_dau)
