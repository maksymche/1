import pandas as pd

# Читаємо CSV (тут файл у тій же папці, що і .py)
df = pd.read_csv("trades.csv")

# Подивитися перші 5 рядків
print(df.head())