import pandas as pd
from pathlib import Path

project_dir = Path(__file__).parent
output_dir = project_dir / "output"
output_dir.mkdir(exist_ok=True)

gold = pd.read_csv(output_dir / "day62_testset.csv")
v1 = pd.read_csv(project_dir / "day63_v1_pred.csv")
v2 = pd.read_csv(project_dir / "day63_v2_pred.csv")

def as_bool(series):
    return series.astype(str).str.lower().eq("true")

def score(pred, version_name):
    merged = gold.merge(pred, on="case_id", suffixes=("_gold", "_pred"))
    category_ok = merged["category_gold"] == merged["category_pred"]
    human_ok = as_bool(merged["need_human_gold"]) == as_bool(merged["need_human_pred"])
    category_acc = category_ok.mean()
    human_acc = human_ok.mean()
    print(f"\n{version_name}")
    print(f"分类准确率：{category_acc:.1%}")
    print(f"转人工准确率：{human_acc:.1%}")
    print("分类答错的 case_id：", merged.loc[~category_ok, "case_id"].tolist())
    print("转人工答错的 case_id：", merged.loc[~human_ok, "case_id"].tolist())
    return category_acc, human_acc

score(v1, "v1")
score(v2, "v2")