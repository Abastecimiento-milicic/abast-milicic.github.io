import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

for root, dirs, files in os.walk('data'):
    for f in files:
        if f.endswith('.csv'):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='latin1', errors='ignore') as fh:
                    h = fh.readline().strip()
                    for term in ['tipo material', 'tipo de material', 'mtart', 'tipo_mat']:
                        if term in h.lower():
                            print(f"{p} has '{term}' in header")
            except Exception:
                pass
