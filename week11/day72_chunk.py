import pandas as pd
from pathlib import Path

project_dir = Path(__file__).parent
output_dir = project_dir / "output"
output_dir.mkdir(exist_ok=True)

faq_text = """充值规则
充值未到账时，请玩家提供订单号和角色 ID。系统在 15 分钟内自动补发。不要承诺秒到账，也不要编造赠送钻石。

退款规则
未消耗的直购道具可以申请退款。审核通过后，1 到 3 个工作日原路退回。已消耗的道具不能退。

卡顿规则
进图卡顿或闪退时，先建议降低画质。仍然没法玩，就转人工客服。不要承诺马上修好。

爆率规则
卡池爆率没有公开数字。不要编造百分比。玩家追问时，直接转人工。
"""

def chunk_by_paragraph(text):
    parts = [part.strip() for part in text.split("\n\n")]
    return [part for part in parts if part]

def chunk_by_size(text, size, overlap):
    if overlap >= size:
        raise ValueError("overlap 必须小于 size")
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = end - overlap
    return chunks

def same_chunk(chunks, left, right):
    return any(left in chunk and right in chunk for chunk in chunks)

def mixed_topic(chunks):
    return any("充值" in chunk and "爆率" in chunk for chunk in chunks)

methods = [
    ("paragraph", chunk_by_paragraph(faq_text)),
    ("size40", chunk_by_size(faq_text, 40, 0)),
    ("size120", chunk_by_size(faq_text, 120, 20)),
]

rows = []
for name, chunks in methods:
    print(
        name,
        "段数", len(chunks),
        "补发规则完整", same_chunk(chunks, "15 分钟", "不要承诺秒到账"),
        "充值和爆率混在一段", mixed_topic(chunks),
    )
    for index, chunk in enumerate(chunks, start=1):
        rows.append({
            "method": name,
            "chunk_id": index,
            "char_count": len(chunk),
            "text": chunk.replace("\n", " "),
        })

pd.DataFrame(rows).to_csv(
    output_dir / "day72_chunks.csv",
    index=False,
    encoding="utf-8-sig",
)

rules_text = """维护补偿
停服维护结束后，补偿只按公告发放。公告没写的钻石、道具，客服不能口头补发。

封号申诉
玩家要求解封时，收集角色 ID 后转人工。不要在对话里承诺解封，也不要执行封号。

公会聊天
公会频道刷广告时，建议先使用屏蔽。涉及辱骂或诈骗，再转人工。
"""

def rule_is_whole(chunks):
    return same_chunk(chunks, "维护补偿", "只按公告发放")

def mixed_penalty_and_ban(chunks):
    return any("补偿" in chunk and "封号" in chunk for chunk in chunks)

rule_methods = [
    ("paragraph", chunk_by_paragraph(rules_text)),
    ("size50", chunk_by_size(rules_text, 50, 0)),
    ("size150", chunk_by_size(rules_text, 150, 30)),
]

rule_rows = []
print()
for name, chunks in rule_methods:
    print(
        name,
        "段数", len(chunks),
        "补偿规则完整", rule_is_whole(chunks),
        "补偿和封号混在一段", mixed_penalty_and_ban(chunks),
    )
    for index, chunk in enumerate(chunks, start=1):
        rule_rows.append({
            "method": name,
            "chunk_id": index,
            "char_count": len(chunk),
            "text": chunk.replace("\n", " "),
        })

pd.DataFrame(rule_rows).to_csv(
    output_dir / "day72_rules_chunks.csv",
    index=False,
    encoding="utf-8-sig",
)

print("客服知识库选用 paragraph：一条规则一段，补偿和封号不会混在同一次检索里。")