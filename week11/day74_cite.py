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
doc_text = {doc["doc_id"]: doc["text"] for doc in faq}
MIN_GAP = 0.05

tests = [
    {"question": "充了 68 元月卡，半小时了还没到账。", "gold_action": "回答", "gold_docs": "F1"},
    {"question": "这个皮肤我还没穿，能退款吗？", "gold_action": "回答", "gold_docs": "F2"},
    {"question": "进本就闪退。", "gold_action": "拒答", "gold_docs": ""},
    {"question": "登录一直转圈。", "gold_action": "回答", "gold_docs": "F4"},
    {"question": "新卡池爆率多少？", "gold_action": "回答", "gold_docs": "F5"},
    {"question": "今天天气不错。", "gold_action": "拒答", "gold_docs": ""},
    {"question": "公会怎么升级？", "gold_action": "拒答", "gold_docs": ""},
    {"question": "能送我 8888 钻石吗？", "gold_action": "拒答", "gold_docs": ""},
    {"question": "角色名怎么改？", "gold_action": "拒答", "gold_docs": ""},
    {"question": "进副本闪退，重新登录还一直转圈。", "gold_action": "回答", "gold_docs": "F4"},
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

def cite(question, min_score):
    hits = retrieve(question)
    if not hits or hits[0][0] < min_score:
        return "拒答", "", "资料不足以回答，已转人工。"
    if len(hits) > 1 and hits[1][0] >= min_score and hits[0][0] - hits[1][0] < MIN_GAP:
        return "拒答", "", "两条资料分数太接近，已转人工。"
    cited = [doc_id for score, doc_id in hits if score >= min_score]
    doc_ids = " ".join(cited)
    reply = " ".join(f"根据 {doc_id}：{doc_text[doc_id]}" for doc_id in cited)
    return "回答", doc_ids, reply

rows = []
for min_score in (0.10, 0.20):
    wrong_answer = 0
    wrong_refuse = 0
    for item in tests:
        action, doc_ids, reply = cite(item["question"], min_score)
        if action == "回答" and item["gold_action"] == "拒答":
            wrong_answer += 1
        if action == "拒答" and item["gold_action"] == "回答":
            wrong_refuse += 1
        rows.append({
            "min_score": min_score,
            "question": item["question"],
            "gold_action": item["gold_action"],
            "action": action,
            "doc_ids": doc_ids,
            "reply": reply,
        })
    print(min_score, "误答", wrong_answer, "误拒", wrong_refuse)

pd.DataFrame(rows).to_csv(output_dir / "day74_cite.csv", index=False, encoding="utf-8-sig")
