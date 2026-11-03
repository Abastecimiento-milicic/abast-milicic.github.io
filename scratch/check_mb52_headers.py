import sys, csv
sys.stdout.reconfigure(encoding='utf-8')

with open('data/Almacen MB52/Combinados/MB52_CONSOLIDADO_COMBINADO.csv', 'r', encoding='utf-8-sig', errors='ignore') as f:
    reader = csv.reader(f, delimiter=';')
    headers = next(reader)
    print("Headers in MB52_CONSOLIDADO_COMBINADO.csv:")
    for i, h in enumerate(headers):
        print(f"  [{i}] {h!r}")
