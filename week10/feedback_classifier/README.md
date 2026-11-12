# 玩家反馈 AI 分类助手（项目 4）

读取 100 条玩家反馈，调用模型分成类别、情绪、优先级，并记录 Token 成本。少量边界案例另存人工修正，不覆盖模型原结果。

## 怎么运行

在仓库根目录执行：

```bash
python week10/feedback_classifier/classifier.py
```

密钥放在 `week10/.env`，变量名是 `DEEPSEEK_API_KEY`。脚本不会把密钥打出来。

先跑 2 条做检查：

```bash
python week10/feedback_classifier/classifier.py 2
```

## 输入

- `data/feedback.csv`：100 条反馈，含 `case_id`、`feedback`、`case_type`
- `data/human_corrections.csv`：人工复核过的边界案例。字段是 `human_category`、`human_need_human`、`note`

## 输出

- `output/classifications.csv`：每条的模型结果、是否合格、Token 和成本
- `output/review.csv`：模型结果和人工结果并排，并标出有没有改
- `output/new_testset_rows.csv`：只收录改过的行，供下一次 Prompt 对比
- `output/report.md`：条数、成本和修正摘要

## 规则

- 单条最多重试 3 次。429 和 5xx、超时会重试，其它 4xx 不重试。
- 输入按 0.001 元 / 千 Token，输出按 0.004 元 / 千 Token 计。累计达到 0.20 元就停止后面的请求。
- 字段缺失、类别不在允许值里、或者 JSON 不合法时，这一条记失败，后面的反馈继续处理。
- 人工答案写在 `human_category`，不写进 `model_category`。
- 确认过、和模型一致的行不进入新测试集。改过的行必须带 `note`。
