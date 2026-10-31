# 第三方数据采集器（Day 49）

把本周的请求、状态码、超时重试、环境变量和调用日志收成一个脚本。单条失败不会中断整次任务；再运行时会跳过已经成功的目标。

## 怎么运行

在 `week07` 目录下：

```text
python day49_collector.py
```

或在仓库根目录：

```text
python week07/day49_collector.py
```

可选：复制 `.env.example` 为 `.env`，填入 `DEMO_API_KEY`。没有密钥也能采公开接口。不要把 `.env` 提交到 Git。

## 输入

`collector/data/targets.csv`

| 字段 | 含义 |
|---|---|
| name | 目标简称，也是保存 JSON 的文件名 |
| url | GET 地址 |
| timeout | 本次最多等待秒数 |

当前 4 个目标：

| name | 接口 | 预期 |
|---|---|---|
| echo | `https://httpbin.org/get` | 200，回放请求 |
| missing | `https://httpbin.org/status/404` | 404，记失败 |
| slow | `https://httpbin.org/delay/5` | 超时（timeout=1） |
| weather | Open-Meteo 上海当前气温 | 200，含 `current.temperature_2m` |

## 输出（只写 collector/output，不改 data/）

| 文件 | 内容 |
|---|---|
| `output/call_log.csv` | 每次尝试的时间、状态码、耗时、是否成功、错误、重试次数 |
| `output/json/echo.json` | httpbin 回放 |
| `output/json/weather.json` | 天气 JSON |

失败的目标不写 JSON。

## 失败时可恢复

1. 某一个 URL 失败：记下日志，继续采下一个。
2. 脚本中途退出：已写入的 `call_log.csv` 和 JSON 还在。
3. 再运行同一条命令：`ok=True` 的 `name` 会跳过，只补失败项。

## 状态码（本周）

| 码 | 含义 |
|---|---|
| 200 | 成功，正文可用 |
| 400 | 请求有问题 |
| 401 | 未授权 / 钥匙不对 |
| 404 | 地址没有对应资源 |
| 429 | 请求太频繁 |
| 500 | 服务器出错 |

超时会标 `error=timeout`，最多重试 3 次。4xx（除 429）不重试。
