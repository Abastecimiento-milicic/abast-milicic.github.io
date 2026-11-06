import os
import sys
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')

print("Searching for 1001789 across all data files...")

for root, dirs, files in os.walk('data'):
    for f in files:
        if f.endswith('.csv'):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='latin1', errors='ignore') as fh:
                    for line_idx, line in enumerate(fh):
                        if '1001789' in line:
                            print(f"Found in CSV: {p} (line {line_idx+1})")
                            break
            except Exception as e:
                pass
        elif f.endswith('.xlsx') and not 'Combinado' in f:
            p = os.path.join(root, f)
            try:
                df = pd.read_excel(p)
                match = df[df.astype(str).apply(lambda x: x.str.contains('1001789')).any(axis=1)]
                if not match.empty:
                    print(f"Found in XLSX: {p} (cols: {list(df.columns)})")
            except Exception as e:
                pass
