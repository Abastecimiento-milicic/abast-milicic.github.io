import sys, csv
sys.stdout.reconfigure(encoding='utf-8')

with open('data/STO NULO.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f, delimiter=';')
    headers = next(reader)
    print("Headers in STO NULO.csv:")
    for i, h in enumerate(headers):
        if 'alm' in h.lower():
            print(f"  [{i}] {h!r}")
