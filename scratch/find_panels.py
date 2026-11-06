import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'id="panel-resumen"' in l or 'id="panel-servicios"' in l:
        print(f"{i+1}: {l.strip()}")
