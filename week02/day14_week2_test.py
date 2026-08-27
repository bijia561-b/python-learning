features=[
    {
        "name":"反馈","status":"online","call_count":120,"error_count":3,
    },
    {
        "name":"问答","status":"online","call_count":130,"error_count":0,
    },
    {
        "name":"图片","status":"online","call_count":140,"error_count":4,
    },
    {
        "name":"音频","status":"offline","call_count":10,"error_count":0,
    },
    {
        "name":"视频","status":"offline","call_count":20,"error_count":2,
    },
]

error_features=[]
summary_data={
    "功能总数":0,
    "在线功能数":0,
    "总调用次数":0,
    "异常功能数":0,
}

for feature in features:
    summary_data["功能总数"]=summary_data["功能总数"]+1
    summary_data["总调用次数"]=summary_data["总调用次数"]+feature["call_count"]

    if feature["status"]=="online":
        summary_data["在线功能数"]=summary_data["在线功能数"]+1
    
    if feature["error_count"]>0:
        error_features.append(feature)
        summary_data["异常功能数"]=summary_data["异常功能数"]+1

for category,count in summary_data.items():
    print(f"{category}-{count}")
print()

print(f"异常功能数量：{len(error_features)}")
for index,feature in enumerate(error_features,start=1):
    print(f"{index}.{feature['name']}")
print()

for feature in features:
    print(
        f"{feature['name']}-"
        f"{feature['status']}-"
        f"{feature['call_count']}-"
        f"{feature['error_count']}"
    )
   

