import os
import sys
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')

mb52_dir = 'data/Almacen MB52'
for f in sorted(os.listdir(mb52_dir)):
    if f.endswith('.XLSX') or f.endswith('.xlsx'):
        if 'combinado' in f.lower(): continue
        p = os.path.join(mb52_dir, f)
        df = pd.read_excel(p, nrows=2)
        has_tipo = any('tipo' in c.lower() and 'mat' in c.lower() for c in df.columns)
        print(f"{f}: has Tipo material? {has_tipo} -> Cols with 'tipo': {[c for c in df.columns if 'tipo' in c.lower()]}")
