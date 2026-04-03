import sys
import pandas as pd 

print('arguments', sys.argv)

month = sys.argv[1] #0 is always the name of the script and second is arguments

df = pd.DataFrame({"day": [1, 2], "num_pasengers": [3, 4]})
df['month'] = month

print(df.head())

df.to_parquet(f"output_{month}.parquet")

print(f'hello pipeline, month={month}')