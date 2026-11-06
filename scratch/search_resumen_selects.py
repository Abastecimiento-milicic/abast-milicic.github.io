with open('js/resumen.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(k in l for k in ['resumen_obraSelect', 'resumen_anioSelect', 'resumen_mesCumplSelect', 'resumen_gcEmrfSelect']):
        print(f"{i+1}: {l.strip()[:100]}")
