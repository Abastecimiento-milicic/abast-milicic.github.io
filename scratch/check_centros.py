import sys, csv
sys.stdout.reconfigure(encoding='utf-8')

with open('data/CUMPLIMIENTO_OPTIMIZADO.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    centros = set()
    for r in reader:
        c = r.get('CENTRO', '')
        if c: centros.add(c)

print("Values in CENTRO:", sorted(centros))
