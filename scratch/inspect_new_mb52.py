import sys
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')

fpath = 'data/Almacen MB52/Base MB52 378-B.XLSX'
df = pd.read_excel(fpath)
print("New columns in Base MB52 378-B.XLSX:")
print(list(df.columns))

# Search for 1001789
row = df[df['Material'].astype(str).str.contains('1001789', na=False)]
if not row.empty:
    print("\nRow for 1001789:")
    for col in df.columns:
        print(f"  {col}: {row.iloc[0][col]}")
else:
    print("1001789 not found")
