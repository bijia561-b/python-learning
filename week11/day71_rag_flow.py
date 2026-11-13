import pandas as pd
from pathlib import Path

project_dir = Path(__file__).parent
output_dir = project_dir / "output"
output_dir.mkdir(exist_ok=True)

faq = [
    {"doc_id": "F1", "text": "充值未到账时，请玩家提供订单号和角色 ID，系统在 15 分钟内自动补发。不要承诺秒到账。"},
    {"doc_id": "F2", "text": "未消耗的直购道具可以退款，审核通过后 1 到 3 个工作日原路退回。"},
    {"doc_id": "F3", "text": "进图卡顿或闪退时，先建议降低画质。仍然没法玩，就转人工。"},
    {"doc_id": "F4", "text": "登录一直转圈时，先让玩家切换网络。仍然进不去，就转人工。"},
    {"doc_id": "F5", "text": "卡池爆率没有公开数字。不要编造百分比，直接转人工。"},
]

def keywords(text):
    words = ["充值", "到账", "退款", "卡", "闪退", "登录", "转圈", "爆率", "订单"]
    return {word for word in words if word in text}

def retrieve(question):
    question_words = keywords(question)
    scored = []
    for doc in faq:
        overlap = question_words & keywords(doc["text"])
        if overlap:
            scored.append((len(overlap), doc["doc_id"], doc["text"]))
    scored.sort(reverse=True)
    return scored[:1]

def build_prompt(question, hits):
    if not hits:
        return "没有检索到资料。请拒答并转人工，不要编造。"
    return f"只根据资料回答：{hits[0][2]}\n玩家问题：{question}"

questions = [
    "充了 68 元月卡，半小时了还没到账。",
    "下周 SSR 爆率是多少？",
    "今天天气不错。",
]

rows = []
for question in questions:
    hits = retrieve(question)
    doc_id = hits[0][1] if hits else ""
    rows.append({
        "question": question,
        "doc_id": doc_id,
        "prompt": build_prompt(question, hits),
    })
    print(doc_id or "无资料", question)

pd.DataFrame(rows).to_csv(output_dir / "day71_retrieval.csv", index=False, encoding="utf-8-sig")