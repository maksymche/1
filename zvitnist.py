

# агрегація по [client_type + user_id] для того, щоб побачити картину без зайвого ("week_start_date" i "symbol")
agg_client = df.groupby(
    ["client_type", "user_id"]
).agg(
    total_volume=("quantity", "sum"),
    trade_count=("symbol", "count")
).reset_index()


# фільтрування
bronze_only = agg_client[agg_client["client_type"] == "bronze"]
bronze_only_sorted = bronze_only.sort_values(by="total_volume", ascending=False)
bronze_top_three = bronze_only_sorted.head(3)
bronze_top_three = bronze_top_three['user_id'].tolist()
filtered_df = agg[agg["user_id"].isin(bronze_top_three)]


# зберігання результатів
filtered_df.to_excel("output/bronze_top_three.xlsx", index=False)


# графік №1: Volume потижнево
agg2 = df.groupby(
    ["week_start_date"]
).agg(
    total_volume=("quantity", "sum"),
    trade_count=("symbol", "count")
).reset_index()
plt.plot(agg2['week_start_date'], agg2['trade_count'])
plt.show()


# графік №2: bar chart: trade_count по client_type
agg3 = df.groupby(
    ["client_type"]
).agg(
    total_volume=("quantity", "sum"),
    trade_count=("symbol", "count")
).reset_index()
plt.bar(agg3['client_type'], agg3['trade_count'])
plt.show()