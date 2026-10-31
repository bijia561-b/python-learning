# Day 42 第 6 周项目：游戏活动数据看板——将 3 张子图拼成一张看板大图（subplots），并输出复盘与 5 分钟讲解提纲

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 定位项目目录、data 输入目录与 output 输出目录
project_dir=Path(__file__).parent
data_dir=project_dir/"data"
output_dir=project_dir/"output"
output_dir.mkdir(exist_ok=True)

# 1. 计算 DAU 指标（最低日、最高日）
dau_table=pd.read_csv(data_dir/"daily_dau.csv")
dau_table["login_date"]=pd.to_datetime(dau_table["login_date"])

lowest_day=dau_table.loc[dau_table["dau"].idxmin(),"login_date"].date()
lowest_dau=int(dau_table["dau"].min())
highest_day=dau_table.loc[dau_table["dau"].idxmax(),"login_date"].date()
highest_dau=int(dau_table["dau"].max())

# 2. 计算漏斗指标（整体转化率、最大流失环节）
funnel=pd.read_csv(data_dir/"funnel.csv")
steps=funnel["step"].tolist()
users=funnel["users"].tolist()
overall=users[-1]/users[0]

max_drop=-1
max_drop_step=""
for i in range(1,len(users)):
    drop=users[i-1]-users[i]
    if drop>max_drop:
        max_drop=drop
        max_drop_step=f"{steps[i-1]}→{steps[i]}"

# 3. 计算渠道收入指标（主力渠道及占比）
channel_table=pd.read_csv(data_dir/"channel_revenue.csv")
channel_table=channel_table.sort_values("revenue",ascending=False)
highest_channel=channel_table.iloc[0]["channel"]
highest_rate=channel_table.iloc[0]["revenue"]/channel_table["revenue"].sum()

plt.rcParams["font.sans-serif"]=["microsoft yahei","simhei"]
plt.rcParams["axes.unicode_minus"]=False

# 4. plt.subplots(1, 3, figsize=(15, 4)) 创建 1 行 3 列的拼图画布，axes[0]、axes[1]、axes[2] 分别代表左、中、右三块子图
fig,axes=plt.subplots(1,3,figsize=(15,4))

# 左图：DAU 折线图
axes[0].plot(dau_table["login_date"],dau_table["dau"],marker="o")
axes[0].set_title("dau")
axes[0].set_xlabel("日期")
axes[0].set_ylabel("人数")
axes[0].tick_params(axis="x",rotation=30)

# 中图：渠道收入柱状图
axes[1].bar(channel_table["channel"],channel_table["revenue"])
axes[1].set_title("渠道收入")
axes[1].set_xlabel("渠道")
axes[1].set_ylabel("收入")

# 右图：注册到付费横向漏斗图
axes[2].barh(steps,users)
axes[2].invert_yaxis()
axes[2].set_title("漏斗")
axes[2].set_xlabel("人数")

# 调整排版并保存整张看板图片
fig.tight_layout()
fig.savefig(output_dir/"dashboard.png")
plt.close(fig)

# 5. 生成包含结论、建议与 5 分钟讲解提纲的 Markdown 复盘文档
report=f"""#活动数据看板复盘

##结论
- DAU最低出现在{lowest_day}，为{lowest_dau}人；最高出现在{highest_day}，为{highest_dau}人。
- 注册到充值整体转化率为{overall * 100:.1f}%（{users[-1]}/{users[0]}）。
- 流失人数最多的环节是{max_drop_step}，流失{max_drop}人。
- 收入最高渠道是{highest_channel}，占比{highest_rate * 100:.1f}%。

##建议
- 优先排查「{max_drop_step}」：入口是否难找、活动页是否报错。
- 针对{lowest_day}的DAU低点，核对当天投放、故障和统计是否正常。
- {highest_channel}已贡献{highest_rate * 100:.1f}%收入，可优先加投并核对归因是否准确。

##5分钟讲解
1. 打开dashboard.png左图：DAU最低是{lowest_day}的{lowest_dau}人，最高是{highest_day}的{highest_dau}人。
2. 看右图漏斗：整体转化{overall * 100:.1f}%，流失最多的是{max_drop_step}，共{max_drop}人。
3. 看中间柱状图：{highest_channel}占{highest_rate * 100:.1f}%，是当前主力渠道。
4. 建议先改活动入口，再查{lowest_day}当天，投放优先放在{highest_channel}。
"""

report_path=output_dir/"review.md"
report_path.write_text(report,encoding="utf-8")
print("已生成：",output_dir/"dashboard.png")
print("已生成：",report_path)
print(report)
