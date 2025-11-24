from extract_1 import extract_1
from transform_1 import transform_1
from load_1 import load_1

df = extract_1()
df = transform_1(df)
load_1(df)