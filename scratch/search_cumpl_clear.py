with open('js/cumplimiento.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'btnClearFilters' in l or 'cumpl_btnClearFilters' in l:
        print(f"Line {i+1}: {l.strip()[:100]}")
