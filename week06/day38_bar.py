import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

project_dir=Path(__file__).parent
table=pd.read_csv(project_dir/"day38_channel_revenue.csv")
table=table.sort_values("revenue",ascending=False)
print(table)
plt.rcParams["font.sans-serif"]=["Microsoft YaHei","SimHei"]
plt.rcParams["axes.unicode_minus"]=False

plt.bar(table["channel"],table["revenue"])
plt.title("各渠道收入对比")
plt.xlabel("渠道")
plt.ylabel("收入")
plt.tight_layout()

output_dir=project_dir/"output"
output_dir.mkdir(exist_ok=True)
outout_path=output_dir/"day38_channel_bar.png"
plt.savefig(outout_path)
print("已保存:",outout_path)

print("收入最高的渠道：",table.iloc[0]["channel"],table.iloc[0]["revenue"])