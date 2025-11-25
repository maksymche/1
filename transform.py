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
