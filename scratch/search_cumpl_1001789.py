import sys
sys.stdout.reconfigure(encoding='utf-8')

for p in ['data/REPORTE CUMPLIMIENTO.csv', 'data/Base_Final_365_372.csv', 'data/Demoras.csv']:
    try:
        with open(p, 'r', encoding='latin1', errors='ignore') as f:
            headers = f.readline().strip().split(';')
            for line in f:
                if '1001789' in line:
                    print(f"Found in {p}")
                    for h, v in zip(headers, line.strip().split(';')):
                        if any(k in h.lower() for k in ['material', 'item', 'tipo', 'art', 'desc']):
                            print(f"  {h}: {v}")
                    break
    except Exception as e:
        print(f"Error {p}: {e}")
