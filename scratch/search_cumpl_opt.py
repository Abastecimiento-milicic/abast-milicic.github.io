import sys
sys.stdout.reconfigure(encoding='utf-8')

p = 'data/CUMPLIMIENTO_OPTIMIZADO.csv'
with open(p, 'r', encoding='latin1', errors='ignore') as f:
    headers = f.readline().strip().split(';')
    for line in f:
        if '1001789' in line:
            print("Found in CUMPLIMIENTO_OPTIMIZADO.csv:")
            for h, v in zip(headers, line.strip().split(';')):
                print(f"  {h}: {v}")
            break
