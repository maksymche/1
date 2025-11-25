import pandas as pd


# зчитуємо CSV
df = pd.read_csv("trades.csv")





#########





import sqlite3
import pandas as pd


# перетворюємо timestamp у datetime
# конвертуємо коректні дати в datetime, а некоректні - у NaT(NaN)
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")


# видаляємо рядки з NaT
df = df.dropna(subset=["timestamp"])


# формуємо дату початку тижня (понеділок)
df["week_start_date"] = df["timestamp"] - df["timestamp"].dt.weekday * pd.Timedelta(days=1)
df["week_start_date"] = df["week_start_date"].dt.date


# агрегація
agg = df.groupby(
    ["week_start_date", "client_type", "user_id", "symbol"]
).agg(
    total_volume=("quantity", "sum"),
    trade_count=("symbol", "count")
).reset_index()





######





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
