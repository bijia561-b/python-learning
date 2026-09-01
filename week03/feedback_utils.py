def classify_feedback(feedback):
    if feedback is None or feedback.strip()=="":
        return "缺失"
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