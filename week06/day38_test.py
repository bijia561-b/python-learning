import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

project_dir=Path(__file__).parent
table=pd.read_csv(project_dir/"day38_channel_revenue.csv")
table=table.sort_values("revenue",ascending=False)
total=table["revenue"].sum()
highest_channel=table["revenue"].max()
share=table.set_index("channel")["revenue"]


plt.rcParams["font.sans-serif"]=["Microsoft YaHei","SimHei"]
plt.rcParams["axes.unicode_minus"]=False

plt.pie(
    table["revenue"],
    labels=table["channel"],
    autopct="%1.1f%%",
)
plt.title("各渠道收入占比")

output_dir=project_dir/"output"
output_dir.mkdir(exist_ok=True)
output_path=output_dir/"day38_pie_test.png"
plt.savefig(output_path)
print("渠道占比已生成",output_path)
print("占比最高渠道：",share.idxmax(),f"{highest_channel/total*100:.1f}%")