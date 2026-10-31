# Day 21：反馈分类工具模块 feedback_utils.py（封装成独立函数供主程序导入）

def classify_feedback(feedback):
    # 如果传入的是 None，或者去掉首尾空格后是空字符串，归为“缺失”
    if feedback is None or feedback.strip()=="":
        return "缺失"
    # 按关键词依次匹配问题分类
    if "卡顿" in feedback:
        return "性能"
    elif "好友" in feedback:
        return "社交"
    elif "登录" in feedback:
        return "登录"
    elif "充值" in feedback:
        return "付费"
    else:
        return "其它"
