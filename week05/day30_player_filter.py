import pandas as pd
file_path="week05/day29_activity_data.csv"

activity_data=pd.read_csv(file_path)

high_value_players=activity_data[activity_data["recharge"]>=30]

print("充值金额大于30")
print(f"{high_value_players[["player","recharge"]].to_string(index=False)}")

sort=activity_data.sort_values(
    by="recharge",
    ascending=False
)
print(sort.head(3))