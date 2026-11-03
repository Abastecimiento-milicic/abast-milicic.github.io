import sys, glob
sys.stdout.reconfigure(encoding='utf-8')

for f in ['index.html', 'css/base.css']:
    with open(f, 'r', encoding='utf-8') as fh:
        lines = fh.readlines()
    for i, l in enumerate(lines):
        if any(k in l for k in ['cumpl-kpi-num', 'cumpl-row-green', 'cumpl_kpiAT', 'res_cumpl']):
            print(f"{f}:{i+1}: {l.strip()}")
            for j in range(max(0, i-1), min(len(lines), i+6)):
                if j != i:
                    print(f"    {j+1}: {lines[j].strip()}")
