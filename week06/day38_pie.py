# Day 38：绘制饼图（plt.pie）展示各渠道占总收入的比例

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

project_dir=Path(__file__).parent
table=pd.read_csv(project_dir/"day38_channel_revenue.csv")
table=table.sort_values("revenue",ascending=False)
print(table)

plt.rcParams["font.sans-serif"]=["Microsoft YaHei","SimHei"]
plt.rcParams["axes.unicode_minus"]=False

# plt.pie() 用于画饼图，适合看各部分占整体的百分比：
# labels 指定每一块扇区的文字标签；autopct="%1.1f%%" 表示自动算出百分比并保留 1 位小数
plt.pie(
    table["revenue"],
    labels=table["channel"],
    autopct="%1.1f%%",
)
plt.title("各渠道收入占比")

output_dir=project_dir/"output"
output_dir.mkdir(exist_ok=True)
output_path=output_dir/"day38_channel_pie.png"
plt.savefig(output_path)
print("渠道占比已生成",output_path)
