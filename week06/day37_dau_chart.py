import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

project_dir=Path(__file__).parent
table=pd.read_csv(project_dir/"day37_dau.csv")
table["login_date"]=pd.to_datetime(table["login_date"]).dt.date

print(table)

plt.rcParams["font.sans-serif"]=["Microsoft YaHei","SimHei"]
plt.rcParams["axes.unicode_minus"]=False

plt.plot(table["login_date"],table["dau"],marker="o")
plt.title("活动期间DAU趋势")
plt.xlabel("日期")
plt.ylabel("DAU")
plt.xticks(rotation=30)
plt.tight_layout()

lowest_day=table.loc[table["dau"].idxmin(),"login_date"]
lowest_dau=table["dau"].min()

plt.scatter([lowest_day],[lowest_dau],color="red",zorder=5)
plt.annotate(
    f"最低{int(lowest_dau)}",
    xy=(lowest_day,lowest_dau),
    xytext=(10,15),
    textcoords="offset points",
)

output_dir=project_dir/"output"
output_dir.mkdir(exist_ok=True)
output_path=output_dir/"day37_dau_trend.png"
plt.savefig(output_path)
print("已保存：",output_path)

print("dau最低日期:",lowest_day)
print("dau最低值:",lowest_dau)