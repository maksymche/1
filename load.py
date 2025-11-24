

# підключення до бази
conn = sqlite3.connect("agg_result2.db")
cursor = conn.cursor()


# Створення таблиці, якщо ще не існує
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


# Завантаження DataFrame у таблицю (replace=True - перезаписує таблицю)
agg1.to_sql("agg_trades_weekly", conn, if_exists="replace", index=False)


# Закриття з'єднання
conn.close()


print("Дані успішно завантажені у таблицю agg_trades_weekly")