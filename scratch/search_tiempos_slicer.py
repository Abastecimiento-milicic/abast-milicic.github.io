with open('js/tiempos-entrega.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'tiempos_slicer_list' in l or 'slicer' in l.lower():
        print(f"Line {i+1}: {l.strip()[:100]}")
