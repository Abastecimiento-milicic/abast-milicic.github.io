import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

for root, dirs, files in os.walk('data'):
    for f in files:
        if '378' in f or 'MB52' in f or 'ANALISIS' in f:
            print(os.path.join(root, f))
