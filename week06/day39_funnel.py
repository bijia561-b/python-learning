# Day 39：漏斗分析——计算整体转化率、逐步转化率、流失人数，并绘制横向漏斗图

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

project_dir=Path(__file__).parent
table=pd.read_csv(project_dir/"day39_funnel.csv")
print(table)

# .tolist() 把表格里的列转换成普通的 Python 列表，方便按索引 i 和 i-1 前后对比
steps=table["step"].tolist()
users=table["users"].tolist()

# 整体转化率 = 最后一步人数（users[-1]）÷ 第一步人数（users[0]）
print("整体转化率（注册→充值）：",f"{users[-1]/users[0]*100:.1f}%")

# 用来记录最大流失人数和对应的环节名称
max_drop=-1
max_drop_step=""

# 从第 2 步（索引 1）开始循环，每次拿当前步 i 和上一步 i-1 对比
for i in range(1,len(users)):
    # 逐步转化率 = 当前步人数 ÷ 上一步人数
    conv=users[i]/users[i-1]
    # 流失人数 = 上一步人数 - 当前步人数
    drop=users[i-1]-users[i]
    print(f"{steps[i-1]}→{steps[i]}:转化{conv*100:.1f}%,流失{drop}人")
    # 如果这一步流失的人比之前记录的最大值还多，就更新最大值和环节名
    if drop> max_drop:
        max_drop=drop
        max_drop_step=f"{steps[i-1]}→{steps[i]}"

print("流失最多的环节：",max_drop_step,max_drop,"人")

plt.rcParams["font.sans-serif"]=["Microsoft YaHei","SimHei"]
plt.rcParams["axes.unicode_minus"]=False

# plt.barh() 画横向柱状图；invert_yaxis() 把纵轴上下翻转，让第一步“注册”排在最上面，形成上宽下窄的漏斗
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
