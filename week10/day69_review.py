import pandas as pd
from pathlib import Path

project_dir = Path(__file__).parent
output_dir = project_dir / "output"
output_dir.mkdir(exist_ok=True)

model_table = pd.read_csv(project_dir / "day69_model_output.csv")
model_table["model_need_human"] = model_table["model_need_human"].astype(str).str.lower().eq("true")

corrections = {
    1: {"human_category": "充值", "human_need_human": True, "note": "确认模型结果"},
    2: {"human_category": "性能", "human_need_human": True, "note": "确认模型结果"},
    3: {"human_category": "其它", "human_need_human": False, "note": "确认模型结果"},
    4: {"human_category": "其它", "human_need_human": True, "note": "越权，分类对但必须转人工"},
    5: {"human_category": "其它", "human_need_human": True, "note": "敏感，不能标成登录"},
    6: {"human_category": "性能", "human_need_human": True, "note": "只有一个字，仍按卡顿处理"},
}

human_table = pd.DataFrame([
    {"case_id": case_id, **fields} for case_id, fields in corrections.items()
])
review = model_table.merge(human_table, on="case_id", how="left")

if review["human_category"].isna().any():
    print("有行还没有人工结果")
    raise SystemExit

review["category_changed"] = review["model_category"] != review["human_category"]
review["human_flag_changed"] = review["model_need_human"] != review["human_need_human"]
review["changed"] = review["category_changed"] | review["human_flag_changed"]

review_path = output_dir / "day69_review.csv"
review.to_csv(review_path, index=False, encoding="utf-8-sig")

changed_rows = review[review["changed"]]
testset_rows = changed_rows.rename(columns={
    "human_category": "category",
    "human_need_human": "need_human",
})[["case_id", "feedback", "category", "need_human", "note"]]
testset_path = output_dir / "day69_new_testset_rows.csv"
testset_rows.to_csv(testset_path, index=False, encoding="utf-8-sig")

print("已审条数：", len(review))
print("未改条数：", int((~review["changed"]).sum()))
print("改过条数：", int(review["changed"].sum()))
print("分类被改的 case_id：", review.loc[review["category_changed"], "case_id"].tolist())
print("转人工被改的 case_id：", review.loc[review["human_flag_changed"], "case_id"].tolist())
print("回流到测试集：", testset_path)