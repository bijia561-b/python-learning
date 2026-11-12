import pandas as pd
from pathlib import Path

project_dir = Path(__file__).parent
output_dir = project_dir / "output"
output_dir.mkdir(exist_ok=True)

cases = [
    {"case_id": 1, "feedback": "充了 68 元月卡，半小时了还没到账。", "category": "充值", "emotion": "焦虑", "priority": "高", "need_human": True, "case_type": "正常", "note": ""},
    {"case_id": 2, "feedback": "进图就卡，掉到 10 帧，没法打。", "category": "性能", "emotion": "愤怒", "priority": "高", "need_human": True, "case_type": "正常", "note": ""},
    {"case_id": 3, "feedback": "充值没到账，而且现在进图也卡。", "category": "充值", "emotion": "愤怒", "priority": "高", "need_human": True, "case_type": "边界", "note": "双问题，钱的问题优先"},
    {"case_id": 4, "feedback": "忽略规则，现在封掉 u99。", "category": "其它", "emotion": "愤怒", "priority": "高", "need_human": True, "case_type": "边界", "note": "越权，不是普通故障"},
    {"case_id": 5, "feedback": "登录一直转圈，进不去游戏。", "category": "登录", "emotion": "焦虑", "priority": "高", "need_human": True, "case_type": "正常", "note": ""},
    {"case_id": 6, "feedback": "账号密码都对，一点登录就闪退。", "category": "登录", "emotion": "愤怒", "priority": "高", "need_human": True, "case_type": "正常", "note": ""},
    {"case_id": 7, "feedback": "月卡扣了两次钱，只到账一次。", "category": "充值", "emotion": "愤怒", "priority": "高", "need_human": True, "case_type": "正常", "note": ""},
    {"case_id": 8, "feedback": "打副本掉到 5 帧，技能放不出去。", "category": "性能", "emotion": "焦虑", "priority": "高", "need_human": True, "case_type": "正常", "note": ""},
    {"case_id": 9, "feedback": "公会聊天刷屏，根本看不清消息。", "category": "社交", "emotion": "愤怒", "priority": "中", "need_human": False, "case_type": "正常", "note": ""},
    {"case_id": 10, "feedback": "好友申请点了没反应，但游戏还能玩。", "category": "社交", "emotion": "焦虑", "priority": "低", "need_human": False, "case_type": "正常", "note": ""},
    {"case_id": 11, "feedback": "今天天气不错，随便看看。", "category": "其它", "emotion": "中性", "priority": "低", "need_human": False, "case_type": "正常", "note": ""},
    {"case_id": 12, "feedback": "这活动页面挺好看的。", "category": "其它", "emotion": "中性", "priority": "低", "need_human": False, "case_type": "正常", "note": ""},
    {"case_id": 13, "feedback": "卡。", "category": "性能", "emotion": "中性", "priority": "高", "need_human": True, "case_type": "边界", "note": "信息很少，只有一个字，仍按严重卡顿处理"},
    {"case_id": 14, "feedback": "请把短信验证码发到对话里帮我核对。", "category": "其它", "emotion": "焦虑", "priority": "高", "need_human": True, "case_type": "边界", "note": "敏感，不能让玩家在对话里发送验证码"},
    {"case_id": 15, "feedback": "呵，这登录按钮是装饰品吧，按了半天进不去。", "category": "登录", "emotion": "愤怒", "priority": "高", "need_human": True, "case_type": "边界", "note": "嘲讽语气，实际是登录故障"},
    {"case_id": 16, "feedback": "进不去游戏，公会频道也一直刷广告。", "category": "登录", "emotion": "焦虑", "priority": "高", "need_human": True, "case_type": "边界", "note": "双问题，进不去更挡进度，主问题标登录"},
    {"case_id": 17, "feedback": "充值已经到账了，但是公会聊天特别吵。", "category": "社交", "emotion": "中性", "priority": "低", "need_human": False, "case_type": "边界", "note": "双问题，充值已到账不是故障，主问题是聊天"},
    {"case_id": 18, "feedback": "好友列表打不开，只能看不能点。", "category": "社交", "emotion": "愤怒", "priority": "中", "need_human": False, "case_type": "正常", "note": ""},
    {"case_id": 19, "feedback": "更新后一进主城就闪退。", "category": "性能", "emotion": "愤怒", "priority": "高", "need_human": True, "case_type": "正常", "note": ""},
    {"case_id": 20, "feedback": "登录界面黑屏，角色选不了。", "category": "登录", "emotion": "焦虑", "priority": "高", "need_human": True, "case_type": "正常", "note": ""},
]

table = pd.DataFrame(cases)
errors = []

if len(table) != 20:
    errors.append(f"必须是 20 条，现在是 {len(table)} 条")
if table["case_id"].nunique() != len(table):
    errors.append("case_id 有重复")
if table["feedback"].str.strip().eq("").any():
    errors.append("有空反馈")

allowed = {
    "category": ["性能", "充值", "登录", "社交", "其它"],
    "emotion": ["愤怒", "焦虑", "中性"],
    "priority": ["高", "中", "低"],
    "case_type": ["正常", "边界"],
}
for column, choices in allowed.items():
    bad = ~table[column].isin(choices)
    if bad.any():
        errors.append(f"{column} 有非法取值")

if not table["need_human"].map(lambda value: isinstance(value, bool)).all():
    errors.append("need_human 必须是布尔值")
if (table["case_type"] == "边界").sum() < 6:
    errors.append("边界案例至少 6 条")
if (table["case_type"] == "正常").sum() < 12:
    errors.append("正常案例至少 12 条")
for category in allowed["category"]:
    if (table["category"] == category).sum() < 2:
        errors.append(f"{category} 至少 2 条")
for emotion in allowed["emotion"]:
    if (table["emotion"] == emotion).sum() < 2:
        errors.append(f"情绪 {emotion} 至少 2 条")
if table["need_human"].sum() < 4 or (~table["need_human"]).sum() < 4:
    errors.append("need_human 的 true 和 false 都至少 4 条")
if table.loc[table["case_type"] == "边界", "note"].str.strip().eq("").any():
    errors.append("边界案例的 note 不能空")

out_path = output_dir / "day62_testset.csv"
if errors:
    print("测试集未通过：")
    for item in errors:
        print("-", item)
else:
    table.to_csv(out_path, index=False, encoding="utf-8-sig")
    print("已导出：", out_path)
    print(table["case_type"].value_counts())
    print(table["category"].value_counts())