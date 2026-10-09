import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

project_dir=Path(__file__).parent
table=pd.read_csv(project_dir/"day39_funnel.csv")
print(table)

steps=table["step"].tolist()
users=table["users"].tolist()

print("整体转化率（注册→充值）：",f"{users[-1]/users[0]*100:.1f}%")

max_drop=-1
max_drop_step=""

for i in range(1,len(users)):
    conv=users[i]/users[i-1]
    drop=users[i-1]-users[i]
    print(f"{steps[i-1]}→{steps[i]}:转化{conv*100:.1f}%,流失{drop}人")
    if drop> max_drop:
        max_drop=drop
        max_drop_step=f"{steps[i-1]}→{steps[i]}"

print("流失最多的环节：",max_drop_step,max_drop,"人")

plt.rcParams["font.sans-serif"]=["Microsoft YaHei","SimHei"]
plt.rcParams["axes.unicode_minus"]=False

plt.barh(steps,users)
plt.gca().invert_yaxis()
plt.title("注册到付费漏斗")
plt.xlabel("人数")
plt.tight_layout()

output_dir=project_dir/"output"
output_dir.mkdir(exist_ok=True)
output_path=output_dir/"day39_funnel.png"
plt.savefig(output_path)
print("漏斗图已导出：",output_path)