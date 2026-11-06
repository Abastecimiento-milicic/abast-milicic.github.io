import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
for f in os.listdir('data'):
    print(f)
