import json
result={
    "feature":"新手引导",
    "status":"需要优化",
    "score":3,
    "issues":["教程太长","提示不够清楚","表达形式单调"],
    "owner":"产品组"
}

result["metrics"]={
    "latency_ms":820,
    "cost":0.03
}

file_path="week03/day21_ai_result.json"

result["issues"].append("奖励说明不清楚")

with open(file_path,"w",encoding="utf-8")as file:
    json.dump(result,file,ensure_ascii=False,indent=2)

try:
    with open(file_path,"r",encoding="utf-8") as file:
        loaded_result=json.load(file)
except FileNotFoundError:
    print("找不到json文件")
except json.JSONDecodeError:
    print("json格式错误")
else:
    print(f"功能：{loaded_result['feature']}")
    print(f"状态：{loaded_result['status']}")
    print(f"评分：{loaded_result['score']}")
    print(f"问题数量：{len(loaded_result['issues'])}")
    print(f"最后一个问题：{loaded_result['issues'][-1]}")
    print(f"延迟：{loaded_result['metrics']['latency_ms']}ms")
    print(f"负责人：{loaded_result['owner']}")