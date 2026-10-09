import pandas as pd 
import matplotlib.pyplot as plt
from pathlib import Path

input_path="week06/day39_test.csv"
output_path="week06/output/day39_test.png"
table=pd.read_csv(input_path)

step=table["step"].tolist()
user=table["users"].tolist()
print("整体转化率：",f"{user[-1]/user[0]*100:.1f}%")

max_drop=-1
max_step_drop=""
min_step_conv=""
min_conv=100
for  i in range(1,len(user)):
    conv=user[i]/user[i-1]
    drop=user[i-1]-user[i]
    print(f"{step[i-1]}→{step[i]}：流失{drop}人，转化率{conv*100:.1f}%")
    if drop>max_drop:
        max_drop=drop
        max_step_drop=f"{step[i-1]}→{step[i]}"
        conv1=conv
    if conv<min_conv:
        min_conv=conv
        min_step_conv=f"{step[i-1]}→{step[i]}"
        drop1=drop
print(f"流失人数最多的是：{max_step_drop},流失{max_drop}人，转化率为{conv1*100:.1f}%")
print(f"转化率最低的是：{min_step_conv},流失{drop1}人，转化率为{min_conv*100:.1f}%")

plt.rcParams["font.sans-serif"]=["Microsoft YaHei","SimHei"]
plt.rcParams["axes.unicode_minus"]=False

plt.barh(step,user)
plt.gca().invert_yaxis()
plt.title("AI功能漏斗")
plt.xlabel("人数")
plt.tight_layout()

plt.savefig(output_path)
print("test漏斗图已导出")