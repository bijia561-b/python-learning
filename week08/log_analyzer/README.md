# AI 功能调用日志分析器（项目 3）

基于 Python + SQLite + Pandas 的 AI 接口调用监控与成本分析工具。支持一键将 CSV 调用日志导入 SQLite 数据库，自动统计各 AI 功能的成功率、平均耗时、失败次数与用户维度成本，并生成监控分析报告。

## 1. 如何运行

在仓库根目录执行：

```bash
python week08/log_analyzer/analyzer.py
```

或进入项目目录后执行：

```bash
cd week08/log_analyzer
python analyzer.py
```

## 2. 输入与输出文件

### 输入数据（`data/` 目录，只读不修改）
- `data/users.csv`：用户信息表（`user_id`, `user_name`, `vip_level`, `channel`）
- `data/api_calls.csv`：AI 功能调用明细日志（`user_id`, `feature`, `status_code`, `is_success`, `latency_ms`, `cost`, `created_at`）

### 输出产物（脚本自动生成）
- `log_analyzer.db`：SQLite 数据库文件（含 `users` 与 `api_calls` 两张表）
- `output/feature_summary.csv`：按 AI 功能汇总的调用次数、失败次数、成功率、平均耗时与总成本
- `output/user_cost_rank.csv`：关联用户表后的各用户调用次数与累计成本排行榜
- `output/monitor_report.md`：包含全局概览、异常风险定位与优化建议的 Markdown 监控报告

## 3. 监控指标说明

| 指标名称 | 计算公式 / SQL 口径 | 业务含义与监控目的 |
|---|---|---|
| **总调用次数 (`call_count`)** | `COUNT(*)` | 统计功能或全局的请求总量，用来判断业务流量规模与高频功能分布。 |
| **失败次数 (`fail_count`)** | `SUM(1 - is_success)` | 统计状态异常（如 `429` 限流、`500` 服务端报错、`504` 超时）的请求条数，用于快速定位故障最多的功能。 |
| **调用成功率 (`success_rate_pct`)** | `ROUND(AVG(is_success) * 100, 1)`（即 `成功次数 / 总调用次数 × 100%`） | 核心可用性护栏指标；低于阈值（如 95%）说明接口存在报错或限流风险，需优先排查。 |
| **平均耗时 (`avg_latency_ms`)** | `ROUND(AVG(latency_ms), 1)` | 衡量接口响应速度（毫秒）；用于识别慢请求与长耗时功能（如长文本总结），防止用户体验劣化或触发超时。 |
| **最慢单次请求 (`max_latency_ms`)** | `ORDER BY latency_ms DESC LIMIT 1` | 定位极端慢请求发生的时间、用户、状态码与耗时，排查网关超时（504）或服务端卡顿。 |
| **累计成本 (`total_cost`)** | `ROUND(SUM(cost), 2)` | 统计功能或用户维度的累计花费（元）；结合 `JOIN users` 识别高消耗用户与高成本功能，防止预算超支。 |
