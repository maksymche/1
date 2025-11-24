import pandas as pd

# Читаємо CSV (тут файл у тій же папці, що і .py)
df = pd.read_csv("trades.csv")

# Подивитися перші 5 рядків
print(df.head())



##########




import sqlite3
import pandas as pd


# перетворюємо timestamp у datetime
# конвертуємо коректні дати в datetime, а некоректні - у NaT(NaN)
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")


# 2. Видаляємо рядки з NaT
df = df.dropna(subset=["timestamp"])


# формуємо дату початку тижня (понеділок)
df["week_start_date"] = df["timestamp"] - df["timestamp"].dt.weekday * pd.Timedelta(days=1)
df["week_start_date"] = df["week_start_date"].dt.date

print(df["week_start_date"])

# агрегація
agg1 = df.groupby(
    ["week_start_date", "client_type", "user_id", "symbol"]
).agg(
    total_volume=("quantity", "sum"),
    trade_count=("symbol", "count")
).reset_index()





##########




# підключення до бази
conn = sqlite3.connect("agg_result2.db")
cursor = conn.cursor()

# шлях до репозиторію (тут - поточна папка)
repo_dir = Path(__file__).parent
db_path = repo_dir / "agg_result.db"


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

