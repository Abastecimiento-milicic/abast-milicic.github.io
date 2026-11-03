import sys, re
sys.stdout.reconfigure(encoding='utf-8')

for fn in ['js/cumplimiento.js', 'js/cumplimiento-arriba.js', 'js/resumen.js', 'css/base.css', 'index.html']:
    with open(fn, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print(f"=== {fn} ===")
    for i, l in enumerate(lines):
        if any(w in l for w in ['style.color', '0.78', '78', 'cumpl-kpi-num', 'cumpl-row-', 'delta-pos', 'delta-neg']):
            print(f"  {i+1}: {l.strip()[:130]}")
