import sys, glob, re
sys.stdout.reconfigure(encoding='utf-8')

for f in ['index.html', 'css/base.css', 'js/cumplimiento.js', 'js/cumplimiento-arriba.js', 'js/resumen.js']:
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            lines = fh.readlines()
        for i, l in enumerate(lines):
            if any(k in l for k in ['cumpl_kpiAT', 'res_cumplAcumAT', 'res_cumplAT', '0.78', '78']):
                print(f"{f}:{i+1}: {l.strip()[:120]}")
    except Exception as e:
        print(f"Error {f}: {e}")
