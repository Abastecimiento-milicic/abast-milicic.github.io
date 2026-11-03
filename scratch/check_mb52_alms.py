import sys, csv
sys.stdout.reconfigure(encoding='utf-8')

with open('data/Almacen MB52/Combinados/MB52_CONSOLIDADO_COMBINADO.csv', 'r', encoding='utf-8-sig', errors='ignore') as f:
    reader = csv.DictReader(f, delimiter=';')
    alms = set()
    for r in reader:
        v = r.get('Almacén', '')
        if v: alms.add(v)

print("Values of Almacén in MB52_CONSOLIDADO_COMBINADO.csv:")
for a in sorted(alms):
    print(f"  {a!r}")
