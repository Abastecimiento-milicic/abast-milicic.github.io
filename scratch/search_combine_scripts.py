import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

for root, dirs, files in os.walk('.'):
    if '.git' in root or '.gemini' in root: continue
    for f in files:
        if f.endswith('.py'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fh:
                c = fh.read()
                if 'Combinado' in c or 'MB52_CONSOLIDADO' in c or 'combinar_mb52' in c:
                    print(f"Found in {p}")
