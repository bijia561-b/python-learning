import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

project_dir=Path(__file__).parent
output_dir=project_dir/"output"
output_dir.mkdir(exist_ok=True)

dau_table=pd.read_csv(project_dir/"day37_dau.csv")
dau_table["login_date"]=pd.to_datetime(dau_table["login_date"])

lowest_day=dau_table.loc[dau_table["dau"].idxmin(),"login_date"].date()
lowest_dau=int(dau_table["dau"].min())
highest_day=dau_table.loc[dau_table["dau"].idxmax(),"login_date"].date()
highest_dau=int(dau_table["dau"].max())

funnel=pd.read_csv(project_dir/"day39_funnel.csv")
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

channel_table=pd.read_csv(project_dir/"day38_channel_revenue.csv")
channel_table=channel_table.sort_values("revenue",ascending=False)
highest_channel=channel_table.iloc[0]["channel"]
highest_rate=channel_table.iloc[0]["revenue"]/channel_table["revenue"].sum()

plt.rcParams["font.sans-serif"]=["Microsoft Yahei","SimHei"]
plt.rcParams["axes.unicode_minus"]=False
plt.plot(dau_table["login_date"],dau_table["dau"],marker="o")
plt.title("活动DAU趋势")
plt.xlabel("日期")
plt.ylabel("DAU")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(output_dir/"day41_dau.png")
plt.close()

plt.figure()
plt.pie(
    channel_table["revenue"],
    labels=channel_table["channel"],
    autopct="%1.1f%%",
)
plt.title("各渠道收入占比")
plt.tight_layout()
plt.savefig(output_dir/"day41_channel.png")
plt.close()

plt.figure()
plt.barh(steps,users)
plt.gca().invert_yaxis()
plt.title("注册到付费漏斗")
plt.xlabel("人数")
plt.tight_layout()
plt.savefig(output_dir/"day41_funnel.png")
plt.close()

report=f"""#活动复盘

##结论
-DAU最低出现在{lowest_day}，为{lowest_dau}人；最高出现在{highest_day}，为{highest_dau}人。
-注册到充值整体转化率为{overall*100:.1f}%({users[-1]}/{users[0]})。
-流失人数最多的环节是{max_drop_step}，流失{max_drop}人。
-占比最高的渠道是{highest_channel},占比为{highest_rate*100:.1f}%

##建议
-优先排查‘{max_drop_step}’：入口是否难找，活动页是否报错。
-针对{lowest_day}的DAU低点，核对当天投放、故障和统计是否正常。
-{highest_channel}已贡献{highest_rate*100:.1f}%收入,可优先加投并核对归因是否准确。
"""

report_path=output_dir/"day41_review.md"
report_path.write_text(report,encoding="utf-8")
print("已生成：",report_path)
print(report)