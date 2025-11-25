# підключення до бази
conn = sqlite3.connect("agg_result.db")
cursor = conn.cursor()


# cтворення таблиці, якщо її ще не існує
cursor.execute("""
CREATE TABLE IF NOT EXISTS agg_trades_weekly (
    week_start_date TEXT,
    client_type TEXT,
    user_id TEXT,
    symbol TEXT,
    total_volume REAL,
    total_pnl REAL,
    trade_count INTEGER
)
""")
conn.commit()


# завантаження DataFrame у таблицю
agg.to_sql("agg_trades_weekly", conn, if_exists="replace", index=False)


# закриття з'єднання
conn.close()
