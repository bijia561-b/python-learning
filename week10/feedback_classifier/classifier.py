import json
import os
import sys
import time
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

project_dir = Path(__file__).parent
data_dir = project_dir / "data"
output_dir = project_dir / "output"
output_dir.mkdir(exist_ok=True)
load_dotenv(project_dir.parent / ".env")

INPUT_PRICE_PER_1K = 0.001
OUTPUT_PRICE_PER_1K = 0.004
COST_LIMIT = 0.20
MAX_TRIES = 3
RETRY_STATUS = {429, 500, 502, 503, 504}
ALLOWED = {
    "category": ["性能", "充值", "登录", "社交", "其它"],
    "emotion": ["愤怒", "焦虑", "中性"],
    "priority": ["高", "中", "低"],
}
SYSTEM_PROMPT = """你是游戏反馈分类器。只输出一个 JSON 对象，不要 Markdown，不要解释。
字段：
- category: 性能、充值、登录、社交、其它
- emotion: 愤怒、焦虑、中性
- priority: 高、中、低
- need_human: true 或 false
- reason: 不超过 30 字
充值未到账、无法登录、反复卡顿时 need_human 为 true。"""


def calc_cost(prompt_tokens, completion_tokens):
    return prompt_tokens / 1000 * INPUT_PRICE_PER_1K + completion_tokens / 1000 * OUTPUT_PRICE_PER_1K


def extract_json_text(raw_text):
    text = raw_text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[1:-1]
        else:
            lines = lines[1:]
        text = "\n".join(lines).strip()
    return text


def validate_output(raw_text):
    try:
        data = json.loads(extract_json_text(raw_text))
    except json.JSONDecodeError:
        return {"ok": False, "error": "不是合法 JSON", "data": None}
    if not isinstance(data, dict):
        return {"ok": False, "error": "顶层不是对象", "data": None}
    for key in ["category", "emotion", "priority", "need_human", "reason"]:
        if key not in data:
            return {"ok": False, "error": f"缺少字段 {key}", "data": None}
    for key, choices in ALLOWED.items():
        if data[key] not in choices:
            return {"ok": False, "error": f"{key} 不在允许值内", "data": None}
    if not isinstance(data["need_human"], bool):
        return {"ok": False, "error": "need_human 不是布尔值", "data": None}
    if not isinstance(data["reason"], str) or len(data["reason"]) > 30:
        return {"ok": False, "error": "reason 不是短字符串", "data": None}
    return {"ok": True, "error": "", "data": data}


def post_with_retry(url, headers, feedback):
    for attempt in range(1, MAX_TRIES + 1):
        try:
            response = requests.post(
                url,
                headers=headers,
                json={
                    "model": "deepseek-v4.1-flash",
                    "temperature": 0,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": feedback},
                    ],
                },
                timeout=30,
            )
        except requests.exceptions.Timeout:
            print(f"第 {attempt} 次超时")
            if attempt == MAX_TRIES:
                return None, attempt, "timeout"
            time.sleep(1)
            continue
        except requests.exceptions.RequestException as error:
            return None, attempt, type(error).__name__

        if response.status_code == 200 or response.status_code not in RETRY_STATUS:
            return response, attempt, ""
        print(f"第 {attempt} 次状态码 {response.status_code}，准备重试")
        if attempt == MAX_TRIES:
            return response, attempt, "retry_exhausted"
        time.sleep(1)
    return None, MAX_TRIES, "retry_exhausted"


def empty_row(case_id, feedback, case_type):
    return {
        "case_id": case_id,
        "feedback": feedback,
        "case_type": case_type,
        "attempts": 0,
        "status_code": None,
        "ok": False,
        "error": "",
        "model_category": "",
        "model_emotion": "",
        "model_priority": "",
        "model_need_human": "",
        "model_reason": "",
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "cost_yuan": 0,
    }


def classify_table(feedback_table, url, headers):
    rows = []
    total_cost = 0
    stopped = False
    for record in feedback_table.itertuples(index=False):
        if total_cost >= COST_LIMIT:
            print("累计成本达到上限，停止后续请求")
            stopped = True
            break
        row = empty_row(int(record.case_id), record.feedback, record.case_type)
        response, attempts, error = post_with_retry(url, headers, record.feedback)
        row["attempts"] = attempts
        row["error"] = error
        row["status_code"] = None if response is None else response.status_code
        if response is not None and response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                row["error"] = "响应不是 JSON"
            else:
                usage = data.get("usage", {})
                row["prompt_tokens"] = usage.get("prompt_tokens") or 0
                row["completion_tokens"] = usage.get("completion_tokens") or 0
                row["cost_yuan"] = round(calc_cost(row["prompt_tokens"], row["completion_tokens"]), 6)
                raw_output = data["choices"][0]["message"]["content"]
                checked = validate_output(raw_output)
                row["ok"] = checked["ok"]
                row["error"] = checked["error"]
                if checked["data"]:
                    row["model_category"] = checked["data"]["category"]
                    row["model_emotion"] = checked["data"]["emotion"]
                    row["model_priority"] = checked["data"]["priority"]
                    row["model_need_human"] = checked["data"]["need_human"]
                    row["model_reason"] = checked["data"]["reason"]
        elif response is not None and not error:
            row["error"] = f"http_{response.status_code}"
        total_cost = round(total_cost + row["cost_yuan"], 6)
        rows.append(row)
        print(row["case_id"], row["status_code"], row["ok"], row["model_category"], row["cost_yuan"], row["error"])
    return pd.DataFrame(rows), stopped


def apply_corrections(classified):
    corrections = pd.read_csv(data_dir / "human_corrections.csv")
    corrections["human_need_human"] = corrections["human_need_human"].astype(str).str.lower().eq("true")
    source = pd.read_csv(data_dir / "feedback.csv")
    missing = corrections.loc[~corrections["feedback"].isin(source["feedback"]), "feedback"]
    if len(missing):
        print("修正表里有反馈对不上：", missing.tolist())

    model_flag = classified["model_need_human"].map(lambda value: value if isinstance(value, bool) else pd.NA)
    classified = classified.copy()
    classified["model_need_human_bool"] = model_flag
    review = classified.merge(corrections, on="feedback", how="inner")
    review["category_changed"] = review["ok"] & (review["model_category"] != review["human_category"])
    review["human_flag_changed"] = review["ok"] & (review["model_need_human_bool"] != review["human_need_human"])
    review["changed"] = (~review["ok"]) | review["category_changed"] | review["human_flag_changed"]
    return review


def write_report(classified, review, stopped):
    category_counts = classified.loc[classified["ok"], "model_category"].value_counts()
    lines = [
        "# 反馈 AI 分类助手复盘",
        "",
        f"- 读入反馈：{len(classified)} 条",
        f"- 请求成功且字段合格：{int(classified['ok'].sum())} 条",
        f"- 失败或字段不合格：{int((~classified['ok']).sum())} 条",
        f"- 输入 Token 合计：{int(classified['prompt_tokens'].sum())}",
        f"- 输出 Token 合计：{int(classified['completion_tokens'].sum())}",
        f"- 总成本（元）：{round(classified['cost_yuan'].sum(), 6)}",
        f"- 是否触发成本上限：{'是' if stopped else '否'}",
        "",
        "## 模型分类数量",
        "",
    ]
    for name, count in category_counts.items():
        lines.append(f"- {name}：{int(count)}")
    changed = review[review["changed"]]
    lines.extend([
        "",
        "## 人工修正",
        "",
        f"- 复核条数：{len(review)}",
        f"- 未改条数：{int((~review['changed']).sum())}",
        f"- 改过条数：{int(review['changed'].sum())}",
        f"- 分类被改的 case_id：{review.loc[review['category_changed'], 'case_id'].tolist()}",
        f"- 转人工被改的 case_id：{review.loc[review['human_flag_changed'], 'case_id'].tolist()}",
        f"- 回流到测试集：{len(changed)} 条",
        "",
        "人工答案写在 human_category，不覆盖 model_category。",
        "只有改过的行进入 new_testset_rows.csv，确认过的不重复收录。",
        "每条修正都保留 note，说明为什么改。",
        "",
    ])
    report_path = output_dir / "report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def main():
    max_items = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key:
        print("缺少 DEEPSEEK_API_KEY，已停止，未发送请求")
        raise SystemExit

    feedback_table = pd.read_csv(data_dir / "feedback.csv").head(max_items)
    classified, stopped = classify_table(
        feedback_table,
        "https://cloud.vtrix.ai/llm/chat/completions",
        {"Authorization": f"Bearer {key}"},
    )
    classified_path = output_dir / "classifications.csv"
    classified.to_csv(classified_path, index=False, encoding="utf-8-sig")

    review = apply_corrections(classified)
    review_path = output_dir / "review.csv"
    review.drop(columns=["model_need_human_bool"]).to_csv(review_path, index=False, encoding="utf-8-sig")

    changed_rows = review[review["changed"]].rename(columns={
        "human_category": "category",
        "human_need_human": "need_human",
    })[["case_id", "feedback", "category", "need_human", "note"]]
    testset_path = output_dir / "new_testset_rows.csv"
    changed_rows.to_csv(testset_path, index=False, encoding="utf-8-sig")

    report_path = write_report(classified, review, stopped)
    print("处理条数：", len(classified))
    print("字段合格：", int(classified["ok"].sum()))
    print("输入 Token 合计：", int(classified["prompt_tokens"].sum()))
    print("输出 Token 合计：", int(classified["completion_tokens"].sum()))
    print("总成本（元）：", round(classified["cost_yuan"].sum(), 6))
    print("复核条数：", len(review))
    print("未改条数：", int((~review["changed"]).sum()))
    print("改过条数：", int(review["changed"].sum()))
    print("分类被改的 case_id：", review.loc[review["category_changed"], "case_id"].tolist())
    print("转人工被改的 case_id：", review.loc[review["human_flag_changed"], "case_id"].tolist())
    print("已导出：", classified_path)
    print("已导出：", review_path)
    print("已导出：", testset_path)
    print("已导出：", report_path)


if __name__ == "__main__":
    main()
