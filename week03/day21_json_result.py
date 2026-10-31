# Day 21：JSON 读写与 try/except 异常处理（练习 json.dump、json.load 与异常捕获）

import json

# 准备一个嵌套结构的字典（包含字符串、整数、列表），模拟 AI 分析结果
result={
    "feature":"新手引导",
    "status":"需要优化",
    "score":3,
    "issues":["教程太长","提示不够清楚","表达形式单调"],
    "owner":"产品组"
}

# 在字典中新增一个嵌套子字典 metrics
result["metrics"]={
    "latency_ms":820,
    "cost":0.03
}

file_path="week03/day21_ai_result.json"

# 往 issues 列表里再追加一条问题
result["issues"].append("奖励说明不清楚")

# json.dump() 把 Python 字典保存成 JSON 文件
# ensure_ascii=False 保证中文正常显示不转码；indent=2 让文件自动缩进 2 格，方便人类阅读
with open(file_path,"w",encoding="utf-8")as file:
    json.dump(result,file,ensure_ascii=False,indent=2)

# try / except 用于捕获可能发生的错误，防止程序直接崩溃：
try:
    with open(file_path,"r",encoding="utf-8") as file:
        # json.load() 把 JSON 文件读回成 Python 字典
        loaded_result=json.load(file)
except FileNotFoundError:
    # 如果文件路径不对、文件不存在，跳到这里执行
    print("找不到json文件")
except json.JSONDecodeError:
    # 如果 JSON 文件内容被改坏了、格式不合法，跳到这里执行
    print("json格式错误")
else:
    # 如果 try 里面顺利执行没有报错，就进入 else 打印结果
    print(f"功能：{loaded_result['feature']}")
    print(f"状态：{loaded_result['status']}")
    print(f"评分：{loaded_result['score']}")
    print(f"问题数量：{len(loaded_result['issues'])}")
    # [-1] 表示取列表里的倒数第 1 个（即最后一个）元素
    print(f"最后一个问题：{loaded_result['issues'][-1]}")
    # 读取嵌套字典里的字段：先取 ['metrics']，再取 ['latency_ms']
    print(f"延迟：{loaded_result['metrics']['latency_ms']}ms")
    print(f"负责人：{loaded_result['owner']}")
