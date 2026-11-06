with open('js/analisis-mm.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'btnDLMB52' in l or 'MB52' in l or 'Tipo material' in l or '1001789' in l:
        print(f"Line {i+1}: {l.strip()[:100]}")
