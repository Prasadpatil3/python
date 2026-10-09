from pathlib import Path

import pandas as pd

csv_path = Path(__file__).with_name("student.csv")
df = pd.read_csv(csv_path)

s = pd.Series(df["Name"])

print("series:")
print(s)
