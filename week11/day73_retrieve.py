import math
import pandas as pd
from pathlib import Path

project_dir = Path(__file__).parent
output_dir = project_dir / "output"
output_dir.mkdir(exist_ok=True)

faq = [
    {"doc_id": "F1", "text": "充值未到账时，请玩家提供订单号和角色 ID。系统在 15 分钟内自动补发。不要承诺秒到账，也不要编造赠送钻石。"},
    {"doc_id": "F2", "text": "未消耗的直购道具可以申请退款。审核通过后，1 到 3 个工作日原路退回。已消耗的道具不能退。"},
    {"doc_id": "F3", "text": "进图卡顿或闪退时，先建议降低画质。仍然没法玩，就转人工客服。不要承诺马上修好。"},
    {"doc_id": "F4", "text": "登录一直转圈时，先让玩家切换网络。仍然进不去，就转人工。"},
    {"doc_id": "F5", "text": "卡池爆率没有公开数字。不要编造百分比。玩家追问时，直接转人工。"},
]

questions = [
    {"qid": "Q1", "question": "充了 68 元月卡，半小时了还没到账。", "gold": "F1"},
    {"qid": "Q2", "question": "这个皮肤我还没穿，能退款吗？", "gold": "F2"},
    {"qid": "Q3", "question": "进本就闪退。", "gold": "F3"},
    {"qid": "Q4", "question": "登录一直转圈。", "gold": "F4"},
    {"qid": "Q5", "question": "新卡池爆率多少？", "gold": "F5"},
    {"qid": "Q6", "question": "今天天气不错。", "gold": ""},
]

def bigrams(text):
    chars = [char for char in text if not char.isspace()]
    return [chars[i] + chars[i + 1] for i in range(len(chars) - 1)]

vocab = sorted({gram for doc in faq for gram in bigrams(doc["text"])})

def vector(text):
    grams = set(bigrams(text))
    return [1 if gram in grams else 0 for gram in vocab]

def cosine(left, right):
    dot = sum(x * y for x, y in zip(left, right))
    left_norm = math.sqrt(sum(x * x for x in left))
    right_norm = math.sqrt(sum(y * y for y in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)

doc_vectors = [(doc["doc_id"], vector(doc["text"])) for doc in faq]

def retrieve(question, top_k=3):
    question_vector = vector(question)
    scored = []
    for doc_id, doc_vector in doc_vectors:
        score = cosine(question_vector, doc_vector)
        if score > 0:
            scored.append((score, doc_id))
    scored.sort(key=lambda item: item[0], reverse=True)
    return scored[:top_k]

rows = []
for item in questions:
    hits = retrieve(item["question"])
    hit_ids = [doc_id for _, doc_id in hits]
    top1 = hit_ids[0] if hit_ids else ""
    recalled = item["gold"] in hit_ids if item["gold"] else top1 == ""
    print(item["qid"], "Top1", top1 or "无", "召回", recalled, [(round(score, 3), doc_id) for score, doc_id in hits])
    rows.append({
        "qid": item["qid"],
        "question": item["question"],
        "gold": item["gold"],
        "top1": top1,
        "hit_ids": " ".join(hit_ids),
        "recalled": recalled,
    })

pd.DataFrame(rows).to_csv(output_dir / "day73_retrieval.csv", index=False, encoding="utf-8-sig")

extra = "进副本闪退，重新登录还一直转圈。"
extra_hits = retrieve(extra)
print(extra_hits)
extra_ids = [doc_id for _, doc_id in extra_hits]
print("F4 和 F3 都被召回" if "F4" in extra_ids and "F3" in extra_ids else "F4 或 F3 有遗漏")
