import sys, csv
sys.stdout.reconfigure(encoding='utf-8')

with open('data/CUMPLIMIENTO_OPTIMIZADO.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    vals = set()
    for r in reader:
        v = r.get('ALMACEN RECEPCION 1', '')
        if v: vals.add(v)

print("Values in 'ALMACEN RECEPCION 1':")
for v in sorted(vals):
    print(f"  {v!r}")
