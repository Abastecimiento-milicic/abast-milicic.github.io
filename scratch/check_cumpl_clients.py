import sys, csv
sys.stdout.reconfigure(encoding='utf-8')

with open('data/CUMPLIMIENTO_OPTIMIZADO.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    clients = set()
    for r in reader:
        clients.add(r.get('CLIENTE', ''))

print("All unique CLIENTE in CUMPLIMIENTO_OPTIMIZADO.csv:")
for c in sorted(clients):
    print(f"  {c!r}")
