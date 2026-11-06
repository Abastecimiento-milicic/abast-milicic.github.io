with open('js/cumplimiento.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'setArribaMode' in l or 'isArribaActive' in l:
        print(f"Line {i+1}: {l.strip()[:100]}")
