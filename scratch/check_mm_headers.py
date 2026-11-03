import sys, csv
sys.stdout.reconfigure(encoding='utf-8')

with open('data/ANALISIS-MM.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f, delimiter=';')
    headers = next(reader)
    print("All headers in ANALISIS-MM.csv:")
    for i, h in enumerate(headers):
        if 'almac' in h.lower():
            print(f"  [{i}] MATCHES 'almac': {h!r}")
        else:
            print(f"  [{i}] {h!r}")
