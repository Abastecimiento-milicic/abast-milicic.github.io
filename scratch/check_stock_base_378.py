import sys
sys.stdout.reconfigure(encoding='utf-8')

p = 'data/Stock Base Obra 0378.csv'
with open(p, 'r', encoding='latin1', errors='ignore') as f:
    headers = f.readline().strip().split(';')
    print(p, "Headers:", headers)
    for line in f:
        if '1001789' in line:
            print("Found in 378:")
            parts = line.strip().split(';')
            for h, val in zip(headers, parts):
                print(f"  {h}: {val}")
