import sys, glob, re
sys.stdout.reconfigure(encoding='utf-8')

for f in glob.glob('js/*.js'):
    with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
        lines = fh.readlines()
    for i, line in enumerate(lines):
        if re.search(r'find\(.*almac', line, re.IGNORECASE) or re.search(r'almac.*candidat', line, re.IGNORECASE) or re.search(r'COL_.*ALM', line, re.IGNORECASE):
            print(f"{f}:{i+1}: {line.strip()}")
