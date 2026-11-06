with open('js/cumplimiento-arriba.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[:30]):
    print(f"Line {i+1}: {l.strip()[:100]}")
