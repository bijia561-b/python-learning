# Day 49：第 7 周综合复习——支持断点续采（失败可恢复）的第三方数据采集器

import json
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

# 1. 加载环境变量与配置目录路径
project_dir = Path(__file__).parent
load_dotenv(project_dir / ".env")

targets_path = project_dir / "collector" / "data" / "targets.csv"
output_dir = project_dir / "collector" / "output"
json_dir = output_dir / "json"
log_path = output_dir / "call_log.csv"
output_dir.mkdir(exist_ok=True)
json_dir.mkdir(exist_ok=True)

# 最多重试 3 次；如果配置了 DEMO_API_KEY 就放进请求头 headers，没配则用空字典 {}
max_times = 3
key = os.getenv("DEMO_API_KEY")
headers = {"Authorization": f"Bearer {key}"} if key else {}

# 调用日志表的固定列名
columns = [
    "requested_at",
    "name",
    "url",
    "status_code",
    "elapsed_seconds",
    "ok",
    "error",
    "attempts",
]


# 读取历史调用日志（如果之前跑过，就能知道哪些目标已经成功了）
def load_history():
    if not log_path.exists():
        return pd.DataFrame(columns=columns)
    history = pd.read_csv(log_path)
    # 确保 ok 列是布尔值 True / False
    history["ok"] = history["ok"].astype(str).str.lower().isin(["true", "1"])
    return history


# 将更新后的调用日志保存到 CSV
def save_history(history):
    history.to_csv(log_path, index=False, encoding="utf-8-sig")


# 采集单个 URL 的函数（内置最多 3 次重试，且对 400/404 等客户端错误不盲目重试）
def fetch_one(url, timeout):
    last_error = ""
    last_status = None
    last_elapsed = None
    for attempt in range(1, max_times + 1):
        print(f"  第{attempt}次尝试")
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            last_status = response.status_code
            last_elapsed = round(response.elapsed.total_seconds(), 3)
            # 状态码为 200 时解析 JSON 并立即返回成功结果
            if response.status_code == 200:
                return {
                    "ok": True,
                    "status_code": last_status,
                    "elapsed_seconds": last_elapsed,
                    "error": "",
                    "attempts": attempt,
                    "data": response.json(),
                }
            last_error = f"http_{response.status_code}"
            # 如果是 4xx 错误（比如 400、404，且不是 429 限流），重试也没用，直接 break 跳出重试循环
            if response.status_code < 500 and response.status_code != 429:
                break
        except requests.exceptions.Timeout:
            last_error = "timeout"
        except requests.exceptions.RequestException as error:
            last_error = type(error).__name__
        except ValueError:
            # 如果返回正文不是合法的 JSON，记为 invalid_json 并停止重试
            last_error = "invalid_json"
            break
    # 尝试结束后仍未成功，返回失败结果字典
    return {
        "ok": False,
        "status_code": last_status,
        "elapsed_seconds": last_elapsed,
        "error": last_error,
        "attempts": attempt,
        "data": None,
    }


# 2. 主流程：加载历史记录，找出已经成功（ok=True）的目标名称集合 done
history = load_history()
done = set(history.loc[history["ok"], "name"].astype(str)) if len(history) else set()
targets = pd.read_csv(targets_path)

print("密钥：", "已加载" if key else "未配置（公开接口仍可采集）")
print("已成功、将跳过：", done or "无")

# 3. 逐条遍历 targets.csv 中的采集目标
for item in targets.to_dict(orient="records"):
    name = str(item["name"])
    url = str(item["url"])
    timeout = float(item["timeout"])
    print(f"采集 {name}: {url}")

    # 如果之前已经成功采过，直接跳过，只补采失败或未采过的目标
    if name in done:
        print("  已有成功结果，跳过（失败可恢复）")
        continue

    result = fetch_one(url, timeout)
    # 采集成功时，把返回的 JSON 保存到 output/json/{name}.json
    if result["ok"]:
        json_path = json_dir / f"{name}.json"
        json_path.write_text(
            json.dumps(result["data"], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print("  成功，已保存", json_path.name)
    else:
        print("  失败：", result["error"])

    # 每采完一条就立刻把日志追加写入 call_log.csv（哪怕中途断电，前面采过的记录也不会丢）
    row = {
        "requested_at": datetime.now().isoformat(timespec="seconds"),
        "name": name,
        "url": url,
        "status_code": result["status_code"],
        "elapsed_seconds": result["elapsed_seconds"],
        "ok": result["ok"],
        "error": result["error"],
        "attempts": result["attempts"],
    }
    history = pd.concat([history, pd.DataFrame([row])], ignore_index=True)
    history["ok"] = history["ok"].astype(str).str.lower().isin(["true", "1"])
    save_history(history)

# 4. 打印汇总统计
success = int(history["ok"].sum())
fail = int((history["ok"] == False).sum())
print("日志：", log_path)
print("成功：", success, "行；失败：", fail, "行")
print("再跑一次 python day49_collector.py，已成功的目标会跳过")
