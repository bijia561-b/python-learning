def usage(cost,budget):
    if budget<=0:
        return None
    return cost/budget*100

def total_cost(call_count,per_cost):
    return call_count*per_cost

