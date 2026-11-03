import sys, csv
sys.stdout.reconfigure(encoding='utf-8')

with open('data/CUMPLIMIENTO_OPTIMIZADO.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f, delimiter=';')
    headers = next(reader)
    print("Headers in CUMPLIMIENTO_OPTIMIZADO.csv:")
    for i, h in enumerate(headers):
        print(f"  [{i}] {h!r}")
