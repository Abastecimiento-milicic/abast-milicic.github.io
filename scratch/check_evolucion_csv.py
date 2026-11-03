import sys, csv
sys.stdout.reconfigure(encoding='utf-8')

with open("data/EVOLUCION.csv", "r", encoding="utf-8-sig", errors="ignore") as f:
    reader = csv.reader(f, delimiter=';')
    headers = next(reader)
    print("Headers in EVOLUCION.csv:")
    for i, h in enumerate(headers):
        print(f"  [{i}] {h!r}")
    
    col_obra = [h for h in headers if 'obra' in h.lower() or 'alm' in h.lower() or 'cli' in h.lower()]
    print(f"Candidate obra columns: {col_obra}")
    if col_obra:
        idx = headers.index(col_obra[0])
        obras = set()
        for r in reader:
            if idx < len(r): obras.add(r[idx])
        print(f"Unique values in {col_obra[0]}: {sorted(obras)}")
