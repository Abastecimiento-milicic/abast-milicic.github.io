import sys
sys.stdout.reconfigure(encoding='utf-8')

# Search in ANALISIS-MM.csv
with open('data/ANALISIS-MM.csv', 'r', encoding='latin1', errors='ignore') as f:
    headers = f.readline().strip().split(';')
    print("ANALISIS-MM.csv Headers:")
    print(headers)
    found = False
    for line in f:
        if '1001789' in line:
            parts = line.strip().split(';')
            print("Found 1001789 in ANALISIS-MM.csv:")
            for h, p in zip(headers, parts):
                print(f"  {h}: {p}")
            found = True
    if not found:
        print("Material 1001789 NOT FOUND in ANALISIS-MM.csv!")
