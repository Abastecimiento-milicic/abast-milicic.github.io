import sys, glob, re
sys.stdout.reconfigure(encoding='utf-8')

for f in glob.glob('js/*.js') + ['index.html']:
    with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
        lines = fh.readlines()
    for i, line in enumerate(lines):
        if 'almac' in line.lower() and ('${' in line or 'option' in line.lower() or 'select' in line.lower() or 'map' in line.lower()):
            print(f"{f}:{i+1}: {line.strip()[:100]}")
